from RNK_Monitor import get_report
import threading
import time
from collections import deque
from datetime import datetime, timedelta

# --- KONFIGURATION ---
UPDATE_INTERVAL = 5  # Abfrage-Intervall in Sekunden
MAX_CACHE_SIZE = 1000  # Maximale Anzahl an Events im Speicher
MAX_HISTORY_SIZE = 500  # Maximale Anzahl gespeicherter echter Angriffe
COOLDOWN_PERIOD = timedelta(minutes=5)  # Wie lange ein Alarm für dieselbe Signatur stummgeschaltet wird

# --- GLOBALER STATE (SIEM CORE) ---
_lock = threading.Lock()
_current_report = None

# 1. Event Cache & Attack History
# deque mit maxlen sorgt automatisch dafür, dass der Speicher bei alten Events nicht überläuft
_event_cache = deque(maxlen=MAX_CACHE_SIZE)
_attack_history = deque(maxlen=MAX_HISTORY_SIZE)

# 2. Threat State
_threat_state = {
    "current_severity": "LOW",  # LOW, MEDIUM, HIGH, CRITICAL
    "active_incidents": 0,
    "last_updated": None
}

# 3. Alert Cooldowns
# Speichert { "alert_key/signature": timestamp_of_last_alert }
_alert_cooldowns = {}

# 4. Metrics
_metrics = {
    "total_events_processed": 0,
    "total_attacks_detected": 0,
    "alerts_muted_by_cooldown": 0,
    "start_time": datetime.now()
}


# --- SIEM CORE LOGIK ---

def _process_siem_logic(raw_report):
    """
    Das Herzstück des SIEM-Cores. Hier laufen alle deine Zusatzfunktionen zusammen.
    Gesteuert über die empfangenen Daten aus dem Report.
    """
    global _threat_state
    if not raw_report:
        return

    now = datetime.now()
    
    # Extrahiere Events aus dem Report (Struktur hängt von deiner RNK_Monitor API ab)
    # Wir nehmen an, der Report liefert eine Liste von Vorfällen/Events
    events = raw_report.get("events", []) if isinstance(raw_report, dict) else []
    
    # Falls der Report flach ist, simulieren wir ein Event aus dem Report-Inhalt
    if not events and raw_report:
        events = [raw_report]

    new_attacks_in_this_turn = 0

    for event in events:
        _metrics["total_events_processed"] += 1
        
        # 1. Event Cache befüllen
        event_entry = {
            "timestamp": now.isoformat(),
            "data": event
        }
        _event_cache.append(event_entry)

        # Extraktion von Kern-Metadaten für Korrelation & Cooldowns
        # (Passe die Keys an deine tatsächliche Report-Struktur an!)
        event_type = event.get("type", "unknown_signature")
        source_ip = event.get("source_ip", "0.0.0.0")
        is_attack = event.get("is_attack", False) or "danger" in str(event).lower()
        
        if is_attack:
            new_attacks_in_this_turn += 1
            
            # 5. Correlation (Einfaches Regelbeispiel)
            # Wenn dieselbe IP innerhalb des Caches häufiger auftaucht -> Eskalation
            recent_matches_from_ip = sum(
                1 for e in _event_cache 
                if e["data"].get("source_ip") == source_ip and e["data"].get("is_attack")
            )
            
            correlation_tag = "SINGLE_ATTACK"
            if recent_matches_from_ip > 5:
                correlation_tag = "BRUTE_FORCE_SUSPECT"
            elif recent_matches_from_ip > 2:
                correlation_tag = "MULTI_VECTOR_ATTACK"

            # 3. Alert Cooldowns prüfen
            cooldown_key = f"{source_ip}_{event_type}"
            last_alert_time = _alert_cooldowns.get(cooldown_key)

            if last_alert_time and (now - last_alert_time) < COOLDOWN_PERIOD:
                # Event wird verarbeitet, aber Alarmierung/Log wird unterdrückt (Muted)
                _metrics["alerts_muted_by_cooldown"] += 1
                continue 
            
            # Cooldown aktualisieren (Alarm wird ausgelöst)
            _alert_cooldowns[cooldown_key] = now

            # 4. Attack History befüllen
            attack_entry = {
                "detected_at": now.isoformat(),
                "type": event_type,
                "source": source_ip,
                "correlation": correlation_tag,
                "raw_details": event
            }
            _attack_history.append(attack_entry)
            _metrics["total_attacks_detected"] += 1

            # Trigger für ein hypothetisches Alarm-System (z.B. Log, Email, Webhook)
            print(f"[@SIEM ALERT] [{correlation_tag}] {event_type} von {source_ip}!")

    # 2. Threat State Dynamisch berechnen
    _threat_state["active_incidents"] = len(_attack_history) # z.B. offene Angriffe im History-Fenster
    _threat_state["last_updated"] = now.isoformat()
    
    if new_attacks_in_this_turn == 0:
        _threat_state["current_severity"] = "LOW"
    elif new_attacks_in_this_turn < 3:
        _threat_state["current_severity"] = "MEDIUM"
    elif new_attacks_in_this_turn < 6:
        _threat_state["current_severity"] = "HIGH"
    else:
        _threat_state["current_severity"] = "CRITICAL"


# --- THREAD LOGIK ---

def _update_loop():
    global _current_report
    while True:
        try:
            report = get_report()
            with _lock:
                _current_report = report
                # Nach dem Abruf direkt in den SIEM-Core einspeisen
                _process_siem_logic(report)
        except Exception as e:
            print(f"[SIEM-Error] Fehler beim Abrufen/Verarbeiten des Reports: {e}")
            
        time.sleep(UPDATE_INTERVAL)

def start_updater():
    """Starte den SIEM-Core im Hintergrund."""
    thread = threading.Thread(target=_update_loop, daemon=True)
    thread.start()


# --- API / ABFRAGE FUNCTIONS (Für dein Dashboard / Frontend) ---

def get_current_report():
    with _lock:
        return _current_report

def get_siem_status():
    """Liefert den kompletten Sicherheitsstatus für Dashboards."""
    with _lock:
        # Säubere alte Cooldowns aus dem RAM, um Speicherlecks zu verhindern
        now = datetime.now()
        expired_keys = [k for k, t in _alert_cooldowns.items() if (now - t) > COOLDOWN_PERIOD]
        for k in expired_keys:
            del _alert_cooldowns[k]

        return {
            "threat_state": _threat_state.copy(),
            "metrics": _metrics.copy(),
            "event_cache_count": len(_event_cache),
            "attack_history": list(_attack_history),
            "active_cooldowns": len(_alert_cooldowns)
        }

def get_raw_event_cache():
    """Liefert die unstrukturierten Roh-Events im Cache."""
    with _lock:
        return list(_event_cache)
