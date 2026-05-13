# 🏜️ MOJAVE OUTPOST – SECURITY LOGBOOK
📡 Week 3–4 Field Notes (Detection, Nginx, Web Layer Evolution)

„The Mojave doesn’t just record logs… it watches patterns.“

## 📜 OPERATION OVERVIEW
🎯 Mission Focus

Diese Phase dreht sich um:

📡 Log Intelligence (SSH/Auth Logs)
🧠 Detection Thinking (Patterns erkennen)
🐍 Python Security Scripts
🌐 Web Layer Integration (Nginx + Dashboard)
🧱 Infrastructure Debugging (Real-world Issues)

## 🟢 PHASE 1 – LOG INTELLIGENCE (The First Signals)
Die Spurenlese (Log-Analyse)

Ein guter Ranger starrt nicht nur in die Wüste, er liest den Sand. Du hast gelernt, die /var/log/auth.log zu entziffern – das schwarze Brett deines Outposts.

📂 Ziel: SSH-Aktivität verstehen

Analysequelle:

cat /var/log/auth.log
🔍 Filter Tests
❌ Fehlgeschlagene Logins
grep "Failed password" /var/log/auth.log
⚠️ Error Patterns
grep "error" /var/log/auth.log
🧠 Erste Beobachtungen:
SSH Protocol mismatches
Logout errors
Einzelne Authentifizierungsfehler
🧠 Interpretation
Bots / Scanner erzeugen „Noise“
Logs sind kein Debugging-Tool nur für Fehler
Logs sind Verhaltensdaten
🎮 Mini-Discovery

Fragen, die du bereits indirekt beantwortest:

Welche IPs tauchen wiederholt auf?
Gibt es Cluster von Versuchen?
Gibt es zeitliche Muster?

## 🟡 PHASE 2 – DETECTION THINKING (Rule Engine Prototype)
🧠 Erste Sicherheitsregel
IF failed_logins_from_ip > 5 → ALERT
💡 Bedeutung

Du hast hier gebaut:

👉 Mini SIEM Logik (Security Information & Event Thinking)

🧩 Zielstruktur
Input: auth.log
Verarbeitung: IP Aggregation
Output: Alert Event
🎮 Mission Concept
Pattern erkennen
Schwellen definieren
Alarm auslösen
## 🔵 PHASE 3 – PYTHON SECURITY LAYER (Vault Integration)
🧠 Architekturidee

Du hast begonnen zu verbinden:

🐍 Python Scripts
📡 Log Files
🧠 Detection Logic
🧩 geplante Funktion
def check_ssh_attacks():
    pass
🔥 Ziel
Logs lesen
IPs zählen
Threshold triggern
Alert senden
📡 Erweiterungsidee
Telegram Bot Integration
Live Alerts
Event-driven Security
🧠 Bewertung

Das ist bereits:

SOC Lite Engineering

## 🔴 PHASE 4 – REAL WORLD FEEDBACK LOOP
🚨 Erkenntnis:

Logs zeigen echte Bots
Fehlversuche existieren real
Systeme werden aktiv gescannt
💬 Realitätscheck

„Das Internet testet dich immer wie ein Raider.“

## 🟨 PHASE 5 – NGINX INCIDENT (Service Debugging)
🚨 Problem:
systemctl start nginx → failed
🔍 Diagnose
systemctl status nginx

✔ Service läuft bereits

🌐 Netzwerk Check
ss -tulpen | grep :80

✔ Port 80 aktiv

🔥 Root Cause
Service läuft
Problem lag nicht bei nginx selbst

👉 sondern bei:

UFW
AWS Security Group
oder externem Zugriff
🧠 Learning

„Service running ≠ Service reachable“

## 🟦 PHASE 6 – WEB LAYER VALIDATION
🧪 Local Test
curl http://localhost

✔ HTML Response OK

🧠 Interpretation

nginx funktioniert intern
Problem liegt im Netzwerk Layer

## 🟪 PHASE 7 – NETWORK SECURITY REALITY
🔐 UFW Check
sudo ufw status
🚨 Erkenntnis
Port 80 fehlte zunächst
HTTP Zugriff blockiert
🔧 Fix
sudo ufw allow 80
🧠 Security Model
AWS Security Group → äußere Mauer
UFW → innere Mauer
nginx → Service Layer

## 🟧 PHASE 8 – WEB EVOLUTION (STATIC DASHBOARD)
📦 Datei Transfer
scp -i Mojave-Outpost.pem image.jpg RangerJohnson@IP:/home/
📁 Deployment
sudo cp image.jpg /var/www/html/
🌐 Ziel
Bilder & Assets in Web Root verfügbar
Static Web Interface aufgebaut

## 🧠 PHASE 9 – PYTHON + WEB INTEGRATION BUG
❌ Problem 1
ModuleNotFoundError: psutil
🧠 Ursache
Virtual Environment vs System Python mismatch
❌ Problem 2
Permission denied /var/www/html
🧠 Ursache
Linux File Permissions
Root-owned directory
💡 Erkenntnis

„Linux vergibt keine Ausnahmen – nur Rechte.“

## 🧠 CORE SECURITY LESSONS

🔐 Identity Layer
SSH Key = Access Gate
sudo = Privilege Escalation Layer
🧱 Defense Layers
AWS Security Group (outer firewall)
UFW (host firewall)
SSH config (authentication layer)
📡 Observability
auth.log = behavioral dataset
errors ≠ bugs → signals
🧠 Detection Thinking
Threshold-based alerts
Pattern recognition
IP aggregation

## 🏜️ MOJAVE OUTPOST STATUS REPORT
System	Status
IAM	✅ Stable
EC2	✅ Running
SSH	🔐 Hardened
Logs	📡 Actively analyzed
Detection	🧠 Prototype stage
Web Layer	🌐 Partial deployment
Python Stack	🐍 Debugging phase

## 🚀 NEXT EVOLUTION PHASE
🧪 Phase 10 Preview
Live log streaming
Real-time detection engine
Flask API layer
Telegram alert system
Basic SOC dashboard

## 💬 FINAL FIELD NOTE

„You don’t learn security by reading logs.
You learn it by noticing what tries to break them.“

## 🧭 RNK DIRECTIVE

Status:

🟢 Operational
🟡 Under Active Development
🔴 Attack surface continuously observed

<img width="1800" height="1083" alt="Screenshot 2026-05-08 at 14-30-03 Mojave Outpost" src="https://github.com/user-attachments/assets/5fce8fa9-6ad5-4064-a201-22f94d611d38" />


## 📜 MOJAVE OUTPOST: SECURITY LOG [MAI 2026]

Standort: Mojave-Ödland, RNK-Außenposten

## 🛠️ LOGISTIK: DAS ASSET-MANÖVER [07.05.2026]

Um die Moral der Truppe zu stärken, wurde die visuelle Infrastruktur des Terminals aktualisiert.

    Datentransfer: Versorgungsgüter (Bilder) wurden erfolgreich per SCP von der Basis in das Heimverzeichnis des Rangers verschoben.

        scp -i XXX.pem BILD.jpg RangerJohnson@DEINE-IP:/home/RangerJohnson/

    Web-Deployment: Die Assets wurden in das aktive Front-End-Archiv des Außenpostens verlegt:

        sudo cp /home/RangerJohnson/mojave.jpg /var/www/html/

## 🛡️ IAM-STRUKTUR: OPERATION „LEAST PRIVILEGE“ [10.05.2026]

Wir haben die Befehlskette im Cloud-Sektor neu geordnet, um die Sicherheit zu maximieren und die Verantwortlichkeiten zu trennen.

📋 Die neuen Einheiten:
Gruppe,Mitglied,Zugewiesene Berechtigungen (Policies)
RNK (Admins),RangerJohnson,AdministratorAccess (Nur für Notfälle/MFA empfohlen)
OutpostDevOps,MajorKnight,"EC2FullAccess, S3ReadOnly, CloudWatchReadOnly"
SecurityAudit,RangerGhost,"ReadOnlyAccess, CloudWatchReadOnlyAccess"
Karawane,RoseCassidy,IAMUserChangePassword (Minimale Rechte)

Strategische Analyse:
    Identity Separation: Durch die Trennung von Dev, Audit und Standard-Usern wird das Risiko interner Sabotage minimiert.
    Governance: RangerGhost kann nun Logs analysieren, aber keine Systeme verändern – klassisches SOC-Prinzip.

## 🤖 AUTOMATISIERUNG: DER VAULT-WATCHER SERVICE

Das Dashboard ist jetzt kein einfaches Skript mehr, sondern ein echter Linux-Hintergrunddienst (systemd).

🔧 Der Kampf mit dem System-Daemon

Der Weg zur stabilen Überwachung war steinig, wie die Terminal-Logs zeigen:

    Fehlzündung (Unit not found): Ein Ordner wurde fälschlicherweise als .service benannt. Dieser wurde mit sudo rmdir RNK_Watcher.service entfernt.

    Das psutil-Gespenst: Das System meldete ModuleNotFoundError: No module named 'psutil'.

        Ursache: Der Dienst nutzte das globale Python statt der isolierten Umgebung (venv).

    Der finale Fix: Die RNK_Watcher.service wurde so konfiguriert, dass sie das Python-Executable direkt aus dem venv startet.

## 🟢 Status: ACTIVE (RUNNING)

Nach dem Befehl sudo systemctl restart RNK_Watcher.service meldet das System:

    Main PID: 66662 (python3)
    ✅ Keine fehlgeschlagenen Logins erkannt.

Ad Victoriam, Ranger. Die Automatisierung schläft nie! 🫡🏜️
