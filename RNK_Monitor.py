import psutil
from datetime import datetime
import subprocess
import re
from collections import Counter

# Schwellenwerte (eventuell später anpassen)
CPU_LIMIT = 80
RAM_LIMIT = 80
DISK_LIMIT = 90
SSH_FAILED_THRESHOLD = 3 

def check_logins():
    last = subprocess.getoutput("last -n 1")
    return last

def get_failed_logins():
    """Zählt fehlgeschlagene Logins und extrahiert IPs."""
    try:
        # Extrahiert IPs aus fehlgeschlagenen SSH Versuchen
        output = subprocess.getoutput("journalctl -u ssh --since '24h ago' --no-pager | grep 'Failed password'")
        ips = re.findall(r'\b\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}\b', output)
        
        counts = Counter(ips)
        last_failed_ip = ips[-1] if ips else None
        return counts, last_failed_ip
    except Exception:
        return Counter(), None

def detect_sqli(log_path="/var/log/nginx/access.log"):
    """Einfache SQLi Erkennung in Web-Logs."""
    # Beispielhafte Muster für SQL Injection
    patterns = [r"UNION%20SELECT", r"select.*from", r"OR%201=1", r"sleep\("]
    try:
        with open(log_path, "r") as f:
            content = f.read()
            found = [p for p in patterns if re.search(p, content, re.IGNORECASE)]
            return len(found) > 0
    except FileNotFoundError:
        return False
        
def get_suspicious_processes():
    try:
        output = subprocess.getoutput("ps aux --sort=-%cpu | head -n 6")
        lines = output.split("\n")[1:]
        
        suspicious = []
        for line in lines:
            if "root" in line:
                suspicious.append(line)

        return suspicious[:3]
    except Exception:
        return []

def get_threat_level(failed_count):
    """Berechnet das Threat Level."""

    if failed_count >= 20:
        return "RED"

    elif failed_count >= 5:
        return "YELLOW"

    else:
        return "GREEN"
    
def get_system_stats():
    cpu = psutil.cpu_percent(interval=1)
    ram = psutil.virtual_memory().percent
    disk = psutil.disk_usage('/').percent
    
    # Absicherung für Logs
    cpu = cpu if cpu is not None else 0.0
    ram = ram if ram is not None else 0.0
    disk = disk if disk is not None else 0.0
    
    return cpu, ram, disk

def check_limits(cpu, ram, disk):
    warnings = []

    if cpu > CPU_LIMIT:
        warnings.append(f"⚠️ CPU kritisch: {cpu}%")

    if ram > RAM_LIMIT:
        warnings.append(f"⚠️ RAM kritisch: {ram}%")

    if disk > DISK_LIMIT:
        warnings.append(f"⚠️ Speicher kritisch: {disk}%")

    return warnings

def get_report():
    cpu = psutil.cpu_percent(interval=1)
    ram = psutil.virtual_memory().percent
    disk = psutil.disk_usage('/').percent

    failed_counts, last_ip = get_failed_logins()
    total_failed = sum(failed_counts.values())
    sqli_detected = detect_sqli()
    last_login = check_logins()
    
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
        "suspicious": get_suspicious_processes(),
        "last_failed_ip": last_ip,
        "last_login": last_login,
        "failed_ips": dict(failed_counts.most_common(3))
    }
def main():
    cpu, ram, disk = get_system_stats()
    warnings = check_limits(cpu, ram, disk)

    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    print(f"\n📊 Vault Status Report [{timestamp}]")
    print(f"CPU: {cpu}% | RAM: {ram}% | DISK: {disk}%")

    if warnings:
        print("\n🚨 WARNUNG:")
        for w in warnings:
            print(w)
    else:
        print("\n✅ Alles stabil im Vault.")

if __name__ == "__main__":
    main()
