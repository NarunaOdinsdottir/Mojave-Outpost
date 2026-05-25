from datetime import datetime
import system_monitor as sys_mon
import security_monitor as sec_mon
from config import CPU_LIMIT, RAM_LIMIT, DISK_LIMIT
import psutil
from security_monitor import (
    get_failed_logins,
    detect_sqli,
    get_threat_level
)

def main():
    # 1. System-Check
    cpu, ram, disk = sys_mon.get_system_stats()
    warnings = sys_mon.check_limits(cpu, ram, disk)
    
    # 2. Security-Check
    failed_counts, _ = sec_mon.get_failed_logins()
    total_failed = sum(failed_counts.values())
    
    if sec_mon.detect_sqli():
        warnings.append("🚨 SQLi Versuch in Nginx erkannt!")
        
    threat_level = sec_mon.get_threat_level(total_failed)
    if threat_level != "GREEN":
        warnings.append(f"🔥 Erhöhte Bedrohung: {threat_level} ({total_failed} Fehlschläge)")

def get_report():
    cpu = psutil.cpu_percent(interval=1)
    ram = psutil.virtual_memory().percent
    disk = psutil.disk_usage('/').percent

    failed_counts, last_ip = sec_mon.get_failed_logins()
    total_failed = sum(failed_counts.values())
    sqli_detected = sec_mon.detect_sqli()
    last_login = sec_mon.check_logins()
    
    threat_score = (
        total_failed * 1 +
        int(sqli_detected) * 5
)
    threat_level = get_threat_level(total_failed)
    warnings = []
    if cpu > CPU_LIMIT: warnings.append(f"CPU: {cpu}%")
    if ram > RAM_LIMIT: warnings.append(f"RAM: {ram}%")
    if sqli_detected: warnings.append("🚨 SQLi Versuch erkannt!")
    if threat_level != "GREEN" : warnings.append(f"Bedrohungsstufe {threat_level} erkannt!")
    timestamp = datetime.now().strftime("%H:%M:%S")

    return {
        "timestamp": timestamp,
        "cpu": cpu,
        "ram": ram,
        "disk": disk,
        "warnings": warnings,
        "threat_level": get_threat_level(total_failed),
        "failed_logins_count": total_failed,
        "suspicious": sys_mon.get_suspicious_processes(),
        "last_failed_ip": last_ip,
        "last_login": last_login,
        "failed_ips": dict(failed_counts.most_common(3))
    }
    # 3. Ausgabe
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"\n📊 Vault Status Report [{timestamp}]")
    print(f"CPU: {cpu}% | RAM: {ram}% | DISK: {disk}%")

    if warnings:
        print("\n🚨 WARNUNGEN & EVENTS:")
        for w in warnings:
            print(w)
    else:
        print("\n✅ Alles stabil im Vault.")

if __name__ == "__main__":
    main()
