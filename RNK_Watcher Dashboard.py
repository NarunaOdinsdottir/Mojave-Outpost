import os
import time
from RNK_Monitor import get_report
from RNK_Adapter import get_current_report, start_updater

start_updater()

LOGFILE = f"/home/{os.getenv('USER')}/vault_status.log"

def clear():
    os.system("clear")

def get_top_processes():
    raw = os.popen("ps -eo pid,comm,%cpu,%mem,user --sort=-%cpu | head -n 6").read().split("\n")

    processes = []
    
    for line in raw[1:]:  # skip header
        parts = line.split(None, 4)
        if len(parts) < 5:
            continue
        
        pid, command, cpu, mem, user = parts
        
        processes.append({
            "pid": pid,
            "cmd": command[:15],  # kürzen
            "cpu": cpu,
            "mem": mem,
            "user": user
        })

    return processes

def get_last_logs():
    if os.path.exists(LOGFILE):
        return os.popen(f"tail -n 5 {LOGFILE}").read()
    return "Keine Logs gefunden"

def dashboard():
    while True:
        data = get_current_report()
        if not data:
            continue

        processes = get_top_processes()
     
        clear()

        print("🟢 VAULT-OS DASHBOARD")
        print("=" * 40)
        print(f"⏱️ {data['timestamp']}")
        print()

        if data['cpu'] > 80:
            print(f"\033[91m🔥 CPU: {data['cpu']}%\033[0m")
        else:
            print(f"🔥 CPU: {data['cpu']}%")
        
        print(f"🧠 RAM: {data['ram']}%")
        print(f"💾 DISK: {data['disk']}%")
        print()

        print("📊 TOP PROZESSE")
        print("PID   CPU   RAM   USER     PROZESS")
        print("-" * 40)

        for p in processes:
            print(f"{p['pid']:<5} {p['cpu']:>5}% {p['mem']:>5}% {p['user']:<8} {p['cmd']}")

        print("=" * 40)
        print("📜 Threat-Level Logins")
        print(f"STATUS: {data['threat_level']}")
        print(f"Fehlgeschlagene Logins heute: {data['failed_logins_count']}")
        if data['last_failed_ip']:
            print(f"Letzte Angreifer-IP: {data['last_failed_ip']}")

        print("\n🛡️ SECURITY STATUS")
        print("=" * 40)

        print("\n👤 Letzter Login:")
        print(data["last_login"])

        if data["failed_logins_count"] > 0:
            print("\033[91m🚨 LOGIN ANGRIFF!\033[0m")
            print("\n❌ Fehlgeschlagene Logins:")
            for ip, count in data["failed_ips"].items():
                print(f"{ip}: {count} fehlgeschlagene Versuche")
        else:
            print("\n✅ Keine fehlgeschlagenen Logins")

        if data["suspicious"] > 0:
            print("\n⚠️ Auffällige Prozesse:")
            for s, count in data["suspicious"].items():
                print(f"{s}: {count} Auffälligkeiten")
        else:
            print("\n✅ Keine auffälligen Prozesse")

        print("\n" + "=" * 40)
        
        if data["warnings"]:
            print("🚨 WARNUNGEN:")
            for w in data["warnings"]:
                print(w)
        else:
            print("✅ System stabil")

        time.sleep(5)
if __name__ == "__main__":
    dashboard() 
