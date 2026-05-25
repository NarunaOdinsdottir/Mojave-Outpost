import psutil
import subprocess
from config import CPU_LIMIT, RAM_LIMIT, DISK_LIMIT

def get_system_stats():
    cpu = psutil.cpu_percent(interval=1) or 0.0
    ram = psutil.virtual_memory().percent or 0.0
    disk = psutil.disk_usage('/').percent or 0.0
    return cpu, ram, disk

def check_limits(cpu, ram, disk):
    warnings = []
    if cpu > CPU_LIMIT: warnings.append(f"⚠️ CPU kritisch: {cpu}%")
    if ram > RAM_LIMIT: warnings.append(f"⚠️ RAM kritisch: {ram}%")
    if disk > DISK_LIMIT: warnings.append(f"⚠️ Speicher kritisch: {disk}%")
    return warnings

def get_suspicious_processes():
    try:
        output = subprocess.getoutput("ps aux --sort=-%cpu | head -n 6")
        lines = output.split("\n")[1:]
        # Nur Root-Prozesse filtern (Top 3)
        return [line for line in lines if "root" in line][:3]
    except Exception:
        return []
