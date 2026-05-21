from RNK_Monitor import get_report
import threading
import time
from collections import deque
from datetime import datetime, timedelta

# --- KONFIGURATION ---
UPDATE_INTERVAL = 5  # Abfrage des Monitors alle 5 Sekunden
MAX_CACHE_SIZE = 500  # Wie viele historische Reports im RAM bleiben
MAX_HISTORY_SIZE = 100  # Wie viele echte, einzigartige Alarme gespeichert werden
COOLDOWN_PERIOD = timedelta(minutes=5)  # Alarmsperre für dieselbe IP/Angriffsart

# --- GLOBALER SIEM-STATE ---
_lock = threading.Lock()
_current_report = None

# 1. Event Cache & Attack History
_event_cache = deque(maxlen=MAX_CACHE_SIZE)
_attack_history = deque(maxlen=MAX_HISTORY_SIZE)

# 2. Threat State
_threat_state = {
    "current_severity": "LOW",  # LOW, MEDIUM, HIGH, CRITICAL
    "system_health": "HEALTHY",  # HEALTHY, WARNING, CRITICAL
    "active_incidents_count": 0,
    "last_updated": None
}

# 3. Alert Cooldowns
# Speichert { "signatur_oder_ip": timestamp }
_alert_cooldowns = {}

# 4. Metrics
_metrics = {
    "total_scans_performed": 0,
    "total_ssh_failed_detected": 0,
    "total_sqli_detected": 0,
    "alerts_muted_by_cooldown": 0,
    "start_time": datetime.now()
}


# --- SIEM CORE LOGIK ---

def _process_siem_logic(report):
    """
    Analysiert den flachen Report des Monitors und bricht ihn in 
    einzelne, korrelierte SIEM-Ereignisse auf.
    """
    global _threat_state
    if not report:
        return

    now = datetime.now()
    _metrics["total_scans_performed"] += 1

    # 1. Event Cache befüllen (Historie der Roh-Zustände)
    _event_cache.append({
        "received_at": now.isoformat(),
        "report": report
    })

    detected_alerts_this_turn = []

    # --- EXTRAKTION & KORRELATION DER EVENTS ---

    # A) Untersuchung von SSH-Angriffen
    failed_ips = report.get("failed_ips", {})  # Gibt uns die Top 3 IPs und deren Fehlversuche
    last_failed_ip = report.get("last_failed_ip")

    for ip, count in failed_ips.items():
        # Korrelation: Wir prüfen im Cache, ob die Fehlversuche dieser IP steigen
        # Da der Monitor die letzten 24 Stunden zählt, schauen wir, ob JETZT ein neuer Alarm nötig ist
        if count >= 3:  # Unser Schwellenwert für einen Brute-Force-Alarm
            cooldown_key = f"ssh_brute_{ip}"
            last_alert = _alert_cooldowns.get(cooldown_key)

            if last_alert and (now - last_alert) < COOLDOWN_PERIOD:
                _metrics["alerts_muted_by_cooldown"] += 1
            else:
                _alert_cooldowns[cooldown_key] = now
                _metrics["total_ssh_failed_detected"] += 1
                
                # Alarm generieren
                detected_alerts_this_turn.append({
                    "timestamp": now.isoformat(),
                    "type": "SSH_BRUTE_FORCE",
                    "source": ip,
                    "severity": "HIGH" if count >= 20 else "MEDIUM",
                    "description": f"IP {ip} detektiert mit {count} fehlgeschlagenen Logins (24h-Fenster)."
                })

    # B) Untersuchung von SQL-Injections (Web-Logs)
    # Da "detect_sqli" im Monitor bei Fund permanent True liefert, hilft uns der Cooldown hier extrem,
    # nicht alle 5 Sekunden dieselbe Meldung zu triggern.
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
                "timestamp": now.isoformat(),
                "type": "SQL_INJECTION",
                "source": "Nginx Access Log",
                "severity": "HIGH",
                "description": "Bösartige SQL-Muster in den Webserver-Logs erkannt."
            })

    # 4. Attack History aktualisieren
    for alert in detected_alerts_this_turn:
        _attack_history.append(alert)
        # Konsolen-Output als SIEM-Eskalation
        print(f" GRAPHENE-SIEM ALERT [{alert['type']}] - Severity: {alert['severity']} - Msg: {alert['description']}")

    # 2. Threat State & System-Health dynamisch berechnen
    # Hier korrelieren wir Performance-Warnungen mit Sicherheits-Warnungen
    monitor_warnings = report.get("warnings", [])
    has_perf_warning = any(x in "".join(monitor_warnings) for x in ["CPU", "RAM"])
    
    # Bestimme System-Gesundheit
    if has_perf_warning:
        _threat_state["system_health"] = "WARNING"
    else:
        _threat_state["system_health"] = "HEALTHY"

    # Bestimme Bedrohungsstufe (Threat Level) basierend auf der aktuellen Aktivität
    monitor_threat_level = report.get("threat_level", "GREEN")
    
    if len(detected_alerts_this_turn) > 0 or monitor_threat_level == "RED":
        _threat_state["current_severity"] = "CRITICAL"
    elif monitor_threat_level == "YELLOW":
        _threat_state["current_severity"] = "MEDIUM"
    else:
        _threat_state["current_severity"] = "LOW"

    _threat_state["active_incidents_count"] = len(_attack_history)
    _threat_state["last_updated"] = now.isoformat()


# --- THREAD MANAGEMENT ---

def _update_loop():
    global _current_report
    while True:
        try:
            report = get_report()
            with _lock:
                _current_report = report
                # Analysiere den Zustand im SIEM-Core
                _process_siem_logic(report)
        except Exception as e:
            print(f"🚨 [SIEM-CORE ERROR] Fehler bei Verarbeitung: {e}")
            
        time.sleep(UPDATE_INTERVAL)

def start_updater():
    """Startet den SIEM-Core im Hintergrund-Thread."""
    thread = threading.Thread(target=_update_loop, daemon=True)
    thread.start()


# --- EXTERNE API-ABFRAGEN (Für Web-Frontends oder Dashboards) ---

def get_current_report():
    """Liefert den letzten rohen Monitor-Report."""
    with _lock:
        return _current_report

def get_siem_status():
    """
    Das wichtigste Endpunkt-Objekt. Liefert bereinigte Daten, 
    Metriken und die Angriffshistorie für dein SIEM-Dashboard.
    """
    with _lock:
        # Aufräumen abgelaufener Cooldowns, um RAM-Lecks zu verhindern
        now = datetime.now()
        expired_keys = [k for k, t in _alert_cooldowns.items() if (now - t) > COOLDOWN_PERIOD]
        for k in expired_keys:
            del _alert_cooldowns[k]

        return {
            "threat_state": _threat_state.copy(),
            "metrics": _metrics.copy(),
            "active_cooldowns_count": len(_alert_cooldowns),
            "attack_history": list(_attack_history),
            "cached_events_count": len(_event_cache)
        }

def get_raw_cache():
    """Gibt den gesamten rohen Event-Cache aus."""
    with _lock:
        return list(_event_cache)
