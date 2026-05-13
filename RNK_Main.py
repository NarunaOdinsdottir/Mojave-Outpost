import time
from RNK_Monitor import get_report
from RNK_Bot import send_alert

CHECK_INTERVAL = 300  # alle 5 Minuten

if __name__ == "__main__":
    
    print("🚀 Vault-Securitron gestartet...")
    while True:
        report = get_report()
        if report["warnings"]:  # nur bei Warnungen
            asyncio.run(send_alert(bot, report))
        time.sleep(CHECK_INTERVAL)