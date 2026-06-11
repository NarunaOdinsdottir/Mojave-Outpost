from Vault_monitor import get_report
import threading
import time
from collections import deque
from datetime import datetime, timedelta
import os
import json
import logging
from logging.handlers import TimedRotatingFileHandler

# FastAPI & Uvicorn für die Server-Variante
from fastapi import FastAPI
import uvicorn

# --- NEU: FORENSISCHE LOG-ROTATION REGELN ---
LOG_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "forensic_archive")
os.makedirs(LOG_DIR, exist_ok=True)  

FORENSIC_LOG_PATH = os.path.join(LOG_DIR, "siem_incidents.jsonl")

forensic_logger = logging.getLogger("SIEM_Forensics")
forensic_logger.setLevel(logging.INFO)

rotation_handler = TimedRotatingFileHandler(
    FORENSIC_LOG_PATH, 
    when="midnight", 
    interval=1, 
    backupCount=30, 
    encoding="utf-8"
)

formatter = logging.Formatter('%(message)s')
rotation_handler.setFormatter(formatter)
forensic_logger.addHandler(rotation_handler)


# --- KONFIGURATION ---
UPDATE_INTERVAL = 5  
MAX_CACHE_SIZE = 500  
MAX_HISTORY_SIZE = 100  
COOLDOWN_PERIOD = timedelta(minutes=5)  

# --- GLOBALER SIEM-STATE ---
_lock = threading.Lock()
_current_report = None

_event_cache = deque(maxlen=MAX_CACHE_SIZE)
_attack_history = deque(maxlen=MAX_HISTORY_SIZE)

_threat_state = {
    "current_severity": "LOW",  
    "system_health": "HEALTHY",  
    "active_incidents_count": 0,
    "last_updated": None
}

_alert_cooldowns = {}

_metrics = {
    "total_scans_performed": 0,
    "total_ssh_failed_detected": 0,
    "total_sqli_detected": 0,
    "alerts_muted_by_cooldown": 0,
    "start_time": datetime.now()
}


# --- FASTAPI APPLIKATION ---
app = FastAPI(title="Graphene-SIEM Core API", version="2.0.0")

@app.get("/api/v1/status")
def get_api_status():
    """Endpunkt für den Telegram-Bot und Dashboards."""
    with _lock:
        # Wir holen uns den aktuellen SIEM-Zustand
        state = get_siem_status()
        
        # Wir betten die aktuellen Hardware-Auslastungen live ein
        state["system_stats"] = {
            "cpu": _current_report.get("cpu", 0) if _current_report else 0,
            "ram": _current_report.get("ram", 0) if _current_report else 0,
            "disk": _current_report.get("disk", 0) if _current_report else 0
        }
        # Falls es rohe Warnungen gibt, packen wir sie dazu
        state["latest_raw_warnings"] = _current_report.get("warnings", []) if _current_report else []
        
        return state


# --- SIEM CORE LOGIK ---

def _process_siem_logic(report):
    global _threat_state
    if not report:
        return

    now = datetime.now()
    _metrics["total_scans_performed"] += 1

    _event_cache.append({
        "received_at": now.isoformat(),
        "report": report
    })

    detected_alerts_this_turn = []

    # A) SSH-Angriffe
    failed_ips = report.get("failed_ips", {})  
    for ip, count in failed_ips.items():
        if count >= 3:  
            cooldown_key = f"ssh_brute_{ip}"
            last_alert = _alert_cooldowns.get(cooldown_key)

            if last_alert and (now - last_alert) < COOLDOWN_PERIOD:
                _metrics["alerts_muted_by_cooldown"] += 1
            else:
                _alert_cooldowns[cooldown_key] = now
                _metrics["total_ssh_failed_detected"] += 1

                detected_alerts_this_turn.append({
                    "timestamp": now.strftime("%H:%M:%S"),
                    "type": "SSH_BRUTE_FORCE",
                    "source": ip,
                    "severity": "HIGH" if count >= 20 else "MEDIUM",
                    "description": f"IP {ip} detektiert mit {count} fehlgeschlagenen Logins."
                })

    # B) SQL-Injections
    warnings_str = "".join(report.get("warnings", []))
    if "SQLi" in warnings_str:
        cooldown_key = "web_sqli_attack"
        last_alert = _alert_cooldowns.get(cooldown_key)

        if last_alert and (now - last_alert) < COOLDOWN_PERIOD:
            _metrics["alerts_muted_by_cooldown"] += 1
        else:
            _alert_cooldowns[cooldown_key] = now
            _metrics["total_sqli_detected"] += 1

            detected_alerts_this_turn.append({
                "timestamp": now.strftime("%H:%M:%S"),
                "type": "SQL_INJECTION",
                "source": "Nginx Access Log",
                "severity": "HIGH",
                "description": "Bösartige SQL-Muster in den Webserver-Logs erkannt."
            })

    # 4. Attack History aktualisieren & Forensisch archivieren
    for alert in detected_alerts_this_turn:
        _attack_history.append(alert)
        print(f" 🔥 [SIEM ALERT] [{alert['type']}] - Severity: {alert['severity']} - {alert['description']}")

        # FORENSISCHER EXPORT
        try:
            json_line = json.dumps(alert, ensure_ascii=False)
            forensic_logger.info(json_line)
        except Exception as log_err:
            print(f"🚨 [FORENSIC LOG ERROR] Konnte Vorfall nicht archivieren: {log_err}")

    # Threat State & System-Health
    monitor_warnings = report.get("warnings", [])
    has_perf_warning = any(x in "".join(monitor_warnings) for x in ["CPU", "RAM"])
    
    if has_perf_warning:
        _threat_state["system_health"] = "WARNING"
    else:
        _threat_state["system_health"] = "HEALTHY"

    monitor_threat_level = report.get("threat_level", "GREEN")
    
    if len(detected_alerts_this_turn) > 0 or monitor_threat_level == "RED":
        _threat_state["current_severity"] = "CRITICAL"
    elif monitor_threat_level == "YELLOW":
        _threat_state["current_severity"] = "MEDIUM"
    else:
        _threat_state["current_severity"] = "LOW"

    _threat_state["active_incidents_count"] = len(_attack_history)
    _threat_state["last_updated"] = now.strftime("%H:%M:%S")


# --- THREAD MANAGEMENT ---

def _update_loop():
    global _current_report
    while True:
        try:
            report = get_report()
            with _lock:
                _current_report = report
                _process_siem_logic(report)
        except Exception as e:
            print(f"🚨 [SIEM-CORE ERROR] Fehler bei Verarbeitung: {e}")

        time.sleep(UPDATE_INTERVAL)

def _run_fastapi_server():
    """Startet den Uvicorn-Server lokal auf Port 8000."""
    # host="127.0.0.1" bedeutet: Nur lokale Prozesse (wie dein Bot) dürfen anfragen.
    # Wenn du später von außen drauf zugreifen willst, nimm "0.0.0.0"
    uvicorn.run(app, host="127.0.0.1", port=8000, log_level="warning")

def start_updater():
    """Startet sowohl den SIEM-Core als auch den API-Server im Hintergrund."""
    # 1. Start des SIEM-Loops
    core_thread = threading.Thread(target=_update_loop, daemon=True)
    core_thread.start()
    
    # 2. Start des API-Webservers
    api_thread = threading.Thread(target=_run_fastapi_server, daemon=True)
    api_thread.start()
    print("🌐 Graphene-SIEM API-Server wurde auf http://127.0.0.1:8000 gestartet.")


# --- EXTERNE LOGIK-ENDPUNKTE (RAM) ---

def get_current_report():
    with _lock: return _current_report

def get_siem_status():
    with _lock:
        now = datetime.now()
        expired_keys = [k for k, t in _alert_cooldowns.items() if (now - t) > COOLDOWN_PERIOD]
        for k in expired_keys:
            del _alert_cooldowns[k]

        # Serialisierungs-Sicherheit für start_time
        metrics_payload = _metrics.copy()
        if isinstance(metrics_payload.get("start_time"), datetime):
            metrics_payload["start_time"] = metrics_payload["start_time"].isoformat()

        return {
            "threat_state": _threat_state.copy(),
            "metrics": metrics_payload,
            "active_cooldowns_count": len(_alert_cooldowns),
            "attack_history": list(_attack_history),
            "cached_events_count": len(_event_cache)
        }
