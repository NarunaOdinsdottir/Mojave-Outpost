import subprocess
import re
from collections import Counter
from config import SSH_FAIL_PATTERNS, SQLI_PATTERNS

SSH_REGEX = re.compile("|".join(SSH_FAIL_PATTERNS), re.IGNORECASE)

def get_failed_logins():
    """Liest SSH-Logs und filtert flexibel nach der Pattern-Liste."""
    try:
        # Wir holen uns die Logs der letzten 24h OHNE grep, das macht jetzt Python!
        output = subprocess.getoutput("journalctl -u ssh -u sshd --since '24h ago' --no-pager")

        if not output or "No journal files were found" in output:
            return Counter(), None
            
        ips = []
        # Zeile für Zeile durchgehen (schont den RAM bei großen Logs)
        for line in output.splitlines():
            if SSH_REGEX.search(line):
                # IP-Adresse extrahieren
                ip_match = re.search(r'\b\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}\b', line)
                if ip_match:
                    ips.append(ip_match.group(0))

        counts = Counter(ips)
        last_failed_ip = ips[-1] if ips else None
        return counts, last_failed_ip
    except Exception:
        return Counter(), None
        
def check_logins():
    return subprocess.getoutput("last -n 1")
    
def detect_sqli(log_path="/var/log/nginx/access.log"):
    """Prüft Web-Logs gegen SQLi Muster."""
    sqli_regex = re.compile("|".join(SQLI_PATTERNS), re.IGNORECASE)
    try:
        with open(log_path, "r") as f:
            for line in f: # Zeilenweise lesen ist sicherer als f.read()
                if sqli_regex.search(line):
                    return True
        return False
    except FileNotFoundError:
        return False

def get_threat_level(failed_count):
    if failed_count >= 20: return "RED"
    if failed_count >= 5: return "YELLOW"
    return "GREEN"
