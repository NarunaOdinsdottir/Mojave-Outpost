from RNK_Monitor import get_report
import threading
import time

# Intervall in Sekunden
UPDATE_INTERVAL = 5  # z.B. alle 5 Sekunden aktualisieren

# globaler Report
_current_report = None
_lock = threading.Lock()

def _update_loop():
    global _current_report
    while True:
        report = get_report()
        with _lock:
            _current_report = report
        time.sleep(UPDATE_INTERVAL)

def start_updater():
    """Starte Hintergrundthread für automatische Report-Aktualisierung."""
    thread = threading.Thread(target=_update_loop, daemon=True)
    thread.start()

def get_current_report():
    """Liefert immer den aktuellsten Report."""
    with _lock:
        return _current_report