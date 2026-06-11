import time
import sys
from RNK_Adapter import start_updater

if __name__ == "__main__":
    print("🛡️ Graphene-SIEM Backend-Dienst wird initialisiert...")
    
    # Startet den Überwachungs-Loop UND die neue FastAPI-Schnittstelle
    start_updater()
    
    print("🌐 API-Server und Forensik-Archiv sind aktiv.")
    print("🚀 Dienst läuft im Hintergrund. Haupt-Thread schläft...")
    
    # Hält den Haupt-Thread am Leben, ohne CPU-Last zu erzeugen
    try:
        while True:
            time.sleep(3600)
    except (KeyboardInterrupt, SystemExit):
        print("🛑 SIEM-Dienst wird sauber beendet.")
        sys.exit(0)
