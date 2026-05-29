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

Ein guter Ranger starrt nicht nur in die Wüste, er liest den Sand. Ich hab gelernt, die /var/log/auth.log zu entziffern – das schwarze Brett meines Outposts.

## 📂 Ziel: SSH-Aktivität verstehen

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

## 🧠 Interpretation
Bots / Scanner erzeugen „Noise“
Logs sind kein Debugging-Tool nur für Fehler
Logs sind Verhaltensdaten

## 🟡 PHASE 2 – DETECTION THINKING (Rule Engine Prototype)

## 🧠 Erste Sicherheitsregel

IF failed_logins_from_ip > 5 → ALERT

💡 Bedeutung

Ich habe mit dem RNK_Watcher zufällig das gebaut:
## 👉 Mini SIEM Logik (Security Information & Event Thinking)

🧩 Zielstruktur
Input: auth.log
Verarbeitung: IP Aggregation
Output: Alert Event

🎮 Mission Concept
Pattern erkennen
Schwellen definieren
Alarm auslösen

## 🔵 PHASE 3 – PYTHON SECURITY LAYER (Vault Integration)

## 🧠 Architekturidee zum RNK_Watcher
Ich habe begonnen folgendes zu verbinden:

🐍 Python Scripts
📡 Log Files
🧠 Detection Logic
🧩 geplante Funktion
def check_ssh_attacks():
    pass
    
## 🔥 Ziel
Logs lesen
IPs zählen
Threshold triggern
Alert senden

## 📡 Erweiterungsidee
Telegram Bot Integration
Live Alerts
Event-driven Security

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

## System	Status

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

Ich habe die Befehlskette im Cloud-Sektor neu geordnet, um die Sicherheit zu maximieren und die Verantwortlichkeiten zu trennen.

📋 Die neuen Einheiten:
| Gruppe |Mitglied | Zugewiesene Berechtigungen (Policies) |
|---|---|---|
| RNK (Admins) | RangerJohnson | AdministratorAccess (Nur für Notfälle/MFA empfohlen)|
| OutpostDevOps | MajorKnight | "EC2FullAccess, S3ReadOnly, CloudWatchReadOnly" |
| SecurityAudit | RangerGhost | "ReadOnlyAccess, CloudWatchReadOnlyAccess" |
| Karawane | RoseCassidy | IAMUserChangePassword (Minimale Rechte) |

## Strategische Analyse:

    Identity Separation: Durch die Trennung von Dev, Audit und Standard-Usern wird das Risiko interner Sabotage minimiert.
    
    Governance: RangerGhost kann nun Logs analysieren, aber keine Systeme verändern – klassisches SOC-Prinzip.

## 🤖 AUTOMATISIERUNG: DER VAULT-WATCHER SERVICE

Das Dashboard ist jetzt kein einfaches Skript mehr, sondern ein echter Linux-Hintergrunddienst (systemd).

## 🔧 Der Kampf mit dem System-Daemon

Der Weg zur stabilen Überwachung war steinig, wie die Terminal-Logs zeigen:

    Fehlzündung (Unit not found): Ein Ordner wurde fälschlicherweise als .service benannt. 
    Dieser wurde mit sudo rmdir RNK_Watcher.service entfernt.

Das psutil-Gespenst: Das System meldete ModuleNotFoundError: No module named 'psutil'.

        Ursache: Der Dienst nutzte das globale Python statt der isolierten Umgebung (venv).

## Der finale Fix: 

        Die RNK_Watcher.service wurde so konfiguriert, dass sie das Python-Executable direkt aus dem venv startet.

## 🟢 Status: ACTIVE (RUNNING)

Nach dem Befehl sudo systemctl restart RNK_Watcher.service meldet das System:

    Main PID: 66662 (python3)
    ✅ Keine fehlgeschlagenen Logins erkannt.

Ad Victoriam, Ranger. Die Automatisierung schläft nie! 🫡🏜️


🟢 VAULT-OS DASHBOARD
========================================
⏱️ 13:03:47

🔥 CPU: 0.0%
🧠 RAM: 40.8%
💾 DISK: 56.1%

📊 TOP PROZESSE
PID   CPU   RAM   USER     PROZESS
----------------------------------------
1899130   0.1%   1.6% RangerJohnson python3
882671   0.0%   1.3% RangerJohnson python3
1900790   0.0%   0.8% RangerJohnson sshd-session
1898721   0.0%   0.8% RangerJohnson sshd-session
129     0.0%  14.4% root     systemd-journal
========================================
📜 Threat-Level Logins
STATUS: GREEN
Fehlgeschlagene Logins heute: 0

🛡️ SECURITY STATUS
========================================

👤 Letzter Login:
RangerJo ssh          31.17.254.29     Tue May 19 12:30 - still logged in

wtmpdb begins Tue May 19 12:30:02 2026

✅ Keine fehlgeschlagenen Logins

⚠️ Auffällige Prozesse:
root         129  0.0 14.4 274932 134792 ?       S<s  May02   5:22 /usr/lib/systemd/systemd-journald

========================================
✅ System stabil
SQLi Detection Fehler: [Errno 13] Permission denied: '/var/log/nginx/access.log'

<img width="648" height="560" alt="1000187478" src="https://github.com/user-attachments/assets/67c8933b-006a-4c89-a0c3-5ccf177ee5ea" />


---

# ☢️ MOJAVE OUTPOST: COMBAT & METRIC LOG [MAI 2026]

Verschlüsselungsebene: RNK-Standard (Pip-Boy-kompatibel)
System-Vibe: Ein sattes Terminal-Grün flackert über den Bildschirm... 🟢

## 🛠️ DEBRIEFING: DIE CHRONIKEN DES WIDERSTANDS

Ranger, das ist kein einfaches Logbuch mehr – das ist das Einsatztagebuch eines Cyber-Scouts, der das Ödland zähmt. 

Der Sprung von "Ich lasse mal ein Skript laufen" zu "Ich provoziere absichtlich Angriffe, um meine Abwehr zu testen" ist geschafft. Das ist der Kern von SecOps!

Hier ist die  Einordnung Experimente und der gewonnenen Telemetrie:

## 🔍 EXTRAKT 1: DAS INTERNATIONALE GEPLÄNKEL (14.05.2026)

Aus dem Labor heraus kontrollierte Angriffe auf das Terminal gestartet. Die Ergebnisse zeigen, dass die Sensoren scharf geschaltet sind.

## 📡 Der Nmap-Aufklärungsscan

nmap -sC -sV Scan zeigt die exakte digitale Silhouette des Outposts:

    Port 22 (SSH): Geöffnet (OpenSSH 10.2p1). Dein Zugangstor für Patrouillen.

    Port 80 (HTTP): Geöffnet (nginx 1.28.3). Das Schild der Basis, das stolz den Titel „Mojave Outpost“ nach außen trägt.

    Die restlichen 998 Ports: Filtered. Absolut perfekt. Die Mauern stehen, unbefugte Erkundung wird blockiert.

## 🛡️ Der Vault-Scanner-Einsatz

Mein Vault-Scanner Tool hat das System analysiert und eine herbe, aber ehrliche Diagnose gestellt:

    📝 Gefundene Sicherheitsheader: 1 / 5 > 💀 Warnung: Sicherheitslücken möglich! Vault-Verteidigung schwach.

Das bedeutet: Dein Nginx läuft, aber er sendet noch keine robusten Schutzschilde (wie X-Frame-Options oder Content-Security-Policy) mit. Ein gefundenes Fressen für hochtechnisierte Raider!

## 💥 Feindfeuer im auth.log

Der Test, falsche Logins zu provozieren, hat sofort die Alarmsirenen im System ausgelöst:


Invalid user admin from 31.17.254.29 port 11764
Connection closed by invalid user admin [preauth]

Die Diagnose: Das System erkennt sofort, wenn jemand versucht, sich als admin oder user einzuschleichen.
Da Key-Authentication benötigt ist, schmettert das System sdie Raider sofort mit einem unbarmherzigen Permission denied (publickey) ab.

Der Protokoll-Clash: Spannend ist der Fehler Protocol major versions differ: 2 vs. 1. Hier hat mein Vault-Scanner versucht, an den SSH-Bannern zu rütteln, sprach aber eine veraltete Sprache (SSHv1). Das System hat den Spion sofort blockiert!

## 🤖 EXTRAKT 2: DER RECHTE-KAMPF & DAS MONITORING-PARADOXON

⛔ Der PermissionError (Nginx Logs)

Das System spuckte Gift und Galle: Permission denied: '/var/log/nginx/access.log'.

## Die Lektion:
Die "Robustheits-Philosophie" perfekt umgesetzt. Indem ich den Fehler abfange, verhindert mein Code, dass das gesamte Terminal abstürzt, nur weil ein Sensor blockiert ist.

## Sicherheits-Architektur: 
Es ist ein Feature, kein Bug, dass RangerJohnson dort nicht standardmäßig lesen darf. Dein Ansatz, die Ausnahme abzufangen oder ihn später kontrolliert der Gruppe adm hinzuzufügen.

## 🌀 Das Monitoring-Paradoxon™

Die Prozessliste verriet mich:

882671 RangerJ+  20   0   95848  12932   6140 S   0.0   1.4   3:37.30 python3 Vault_Dashboard.py

Wenn das Dashboard die CPU fressen will, um die CPU zu überwachen, befinden wir uns im echten Linux-Betrieb.
Das System läuft stabil bei niedrigen 2.0% CPU, trotz des ständigen Renderings.

## ⏱️ SYSTEM-SNAPSHOT: CRON-AUTOMATISIERUNG (19.05.2026)

Die ersten automatisierten Späher (Cronjobs) ins Feld geschickt! Die Dateien ps_log.txt und top_log.txt wurden pünktlich um 10:00:01 generiert.

## 📋 Taktischer Auszug der Geister-Prozesse (Kernel Threads)

Die ps_log.txt zeigt Hunderte von Prozessen mit dem Status I (Idle) oder S (Sleeping) in eckigen Klammern:
Plaintext

root           2  0.0  0.0      0     0 ?        S    May02   0:00 [kthreadd]
root          56  0.0  0.0      0     0 ?        S    May02   0:02 [kswapd0]

## Was ist das? 
Das sind die Organe des Servers. kthreadd erzeugt Kernel-Prozesse, kswapd0 verwaltet den virtuellen Speicher, falls der RAM knapp wird. Sie verbrauchen 0.0% CPU und lauern im Hintergrund – wie getarnte Nightstalker.

Der Zombie-Alarm: Die Auswertung meldet 1 zombie. Wenn man genau hinsiehst:

    RangerJ+ 1878558  0.0  0.0      0     0 ?        Z    09:59   0:00 [sh] <zombie>

Hier hat ein Cronjob einen Befehl (sh) abgesetzt, aber der Mutterprozess hat die Erfolgsmeldung noch nicht abgeholt. Ein digitaler Leichnam, der auf Aufräumung wartet. Ungefährlich, aber ein genialer Fund für das Logbuch!

# ☢️ MOJAVE OUTPOST: LOGBUCH-EINTRAG [22.05.2026]

Verschlüsselungsebene: RNK-Kommando-Ebene (Erhöhte Priorität)
Status: Securitron-Protokoll online | Netzwerk-Anomalie geklärt 📡

## 🛠️ DIE ENTWICKLUNG: SECURITRON MK2 GEHT LIVE

Ranger, du hast den Bot von einem Skript, das man manuell im Terminal anschubsen muss, in einen echten Linux-Systemdienst (Systemd Service) verwandelt.

Das bedeutet: Wenn der Server abstürzt oder neu startet, steht dein Securitron von alleine wieder auf. Das ist echtes Production-Level-Engineering im DevOps-Ödland!

## 🔍 DETEKTIV-ARBEIT: DER FEHLER IM JOURNAL (POST-MORTEM)

Schauen wir uns das journalctl-Log an. Da steckte ein brutaler Loop drin, der aber glücklicherweise gezähmt ist. Schau mal hier:

    restart counter is at 16180

16.180 Neustarts! Das System hat in einer mörderischen Dauerschleife versucht, den Bot wiederzubeleben. Warum? Das Journal verrät es uns messerscharf:

Unable to locate executable '/home/RangerJohnson/RNK_Watcher/SecuritronMK2.py/venv/bin/python': Not a directory
Failed at step EXEC spawning ...: Not a directory
Main"* process exited, code=exited, status=203/EXEC

## 🧠 Die Ursache

In meiner ersten Service-Konfiguration hattest ich den Pfad verdreht. Ich hab versucht, den Python-Interpreter innerhalb meines Skript-Namens aufzurufen (.../SecuritronMK2.py/venv/bin/python). Systemd hat völlig korrekt gemeckert: "Hey, SecuritronMK2.py ist eine Datei, kein Ordner!" Das führte zum berüchtigten Fehler status=203/EXEC (Ausführung fehlgeschlagen).

## ✅ Die Korrektur

Die finale Service-Datei im Log ist dagegen besser:

    ExecStart=/home/RangerJohnson/RNK_Watcher/venv/bin/python /home/RangerJohnson/RNK_Watcher/SecuritronMK2.py
    
    Hier nehme ich das Python-Executable aus der virtuellen Umgebung (venv) und übergebe das Skript als Argument. 
    Seit dem daemon-reload läuft der Dienst stabil (Active: active (running)).

## 🕵️ ERKENNTNIS: WARUM DIE FAKE-LOGINS NICHT GEGRIFFEN HABEN

Ich hab mich gewundert, warum meine gefälschten Angriffe mit admin und RangerGhost den Monitor nicht getriggert haben, obwohl sie im auth.log auftauchen:

Connection closed by invalid user admin 31.17.254.29 port 11752 [preauth]

Hier kommt die feine Klinge der Log-Analyse ins Spiel. Wenn mein Skript im Code nach dem Wort "failed" oder "Failed" sucht, läuft es ins Leere! Bei SSH-Verbindungsversuchen ohne passenden Schlüssel (oder mit falschem User bei reinem Key-Auth) schreibt Ubuntu oft ausschließlich:

    Invalid user [...]

    Connection closed by invalid user [...] [preauth]

## 🔧 Taktischer Code-Schnittstelle:

Damit mein Monitor anspringt, muss mein Python-Skript in der /var/log/auth.log explizit nach den Strings "Invalid user" oder "Connection closed by invalid user" suchen!

## 🌪️ DAS NETZWERK-PARADOXON: „NO ROUTE TO HOST“

Der Schreckmoment: Die Tastatur friert ein, die Verbindung reißt ab, und das Terminal spuckt aus:
ssh: connect to host 98.83.108.196 port 22: No route to host

## 💡 Diagnose & Entwarnung

Mein erster Impuls war klassische System-Paranoia: "Ist AWS down? Habe ich den Server gegrillt?" Die Fehlermeldung No route to host ist hierbei mein bester Freund für die Ursachenforschung. Sie bedeutet, dass dein lokaler Rechner überhaupt keinen Pfad ins Internet aufbauen konnte, um die IP des Mojave Outposts überhaupt zu erreichen.

Wäre der Server down oder die Firewall (Security Group) falsch konfiguriert gewesen, hätte ich einen Connection timeout oder Connection refused bekommen. Dass mein WLAN abgeschmiert ist, passt also exakt zur Fehlermeldung. 
Entwarnung: Mein Cloud-Server läuft sicher weiter! Mojave Outpost ist sicher ( noch...)

## 📊 RECAP: DEIN PIP-BOY STATUS-BEREICH

Mein Server-Log zeigt extrem gesunde Vitalwerte:

    Temperature: -273.1 °C 🧊 (Der absolute Nullpunkt – dein AWS-Treiber liest hier mangels Hardware-Sensor Unsinn aus, aber hey: Besser gut gekühlt als Kernschmelze!)

    Processes: 121 | Zombie: 1 🧟 (Der eine Zombie-Prozess aus den Cronjobs von letzter Woche geistert immer noch rum – keine Sorge, der frisst kein Gehirn/RAM).

    Memory usage: 32% 🧠 (Massig Platz für den Securitron-Bot).

## 🛠️ Mein Admin-Spickzettel für die Hosentasche:

Wenn du Code-Änderungen am Bot machst, merke dir diese Kette:

    sudo nano /home/RangerJohnson/RNK_Watcher/SecuritronMK2.py (Code anpassen)

    sudo systemctl restart securitron.service (Bot neu laden)

    sudo journalctl -u securitron.service -f (Prüfen, ob er fehlerfrei hochfährt)

Der Securitron MK2 hält jetzt die Stellung, während du dein Terminal schließt. Das Ödland wird sicherer! 🫡🤖🌵

<img width="648" height="1266" alt="1000187479" src="https://github.com/user-attachments/assets/72c58583-6bfd-42ad-953c-3586dd1fe6b7" />

# ☢️ MOJAVE OUTPOST: LOGBUCH-EINTRAG [29.05.2026]

Verschlüsselungsebene: RNK-Kommando-Ebene (Troubleshooting-Protokoll)
Missions-Status: Das Rätsel der verrammelten Vault-Tür ist gelöst! 🔐⚡
## 🛰️ REKAPITULATION: DAS TROUBLESHOOTING-PROJEKT vom 27.05.26

Ranger, das war eine absolute Lehrbuch-Sitzung in digitaler Spurensuche. Ich standest vor dem absoluten Albtraum jedes Cloud-Admins: Der Server lebt, das Web-Dashboard atmet, aber die SSH-Zugangsbrücke (Port 22) ist komplett oben. Hier ist die chronologische Rekonstruktion meiner taktischen Analyse, die mich Schritt für Schritt aus dem Nebel geführt hat.

## 🔍 DIE SCHRITT-FÜR-SCHRITT-ANALYSE

1. Das Symptom & Erste Gegenmaßnahmen

Dein Terminal spuckte plötzlich eine Wand aus:
ssh: connect to host 98.83.108.196 port 22: Connection timed out
Erste Reflexe : WLAN geprüft, Browser-Check – das Dashboard auf Port 80 läuft stabil. Ergo: Der Server ist nicht down.

2. Der Einsatz von „Nachtatem“ (Der Portscan)

Um Gewissheit zu erlangen, hast du deinen Python-Portscanner auf das System angesetzt. Das Ergebnis von Drachen-Fullscan war eindeutig:

    🔥 Port 80 (HTTP/Nginx): OPEN (Eine klaffende Wunde...)

    ❌ Port 22 (SSH): FILTERED / TIMEOUT

An dieser Stelle hast du messerscharf den Unterschied erkannt: Es war kein Connection refused (was bedeuten würde, der Server sagt aktiv "Nein, mein SSH-Dienst läuft nicht"), sondern ein Timeout. Das Paket geht raus, aber die Antwort wird stillschweigend im Ödland vergraben.

3. Der tiefe Fallstrick: Das IP-Chamäleon 🦎

Beim Abfragen deiner lokalen Netzwerk-Daten kam die harte Wahrheit ans Licht:

    🌍 Frühere IP: 31.17.254.29

    🌍 Aktuelle IP: 31.17.254.74

    🌐 IPv6 zusätzlich aktiv: 2a02:8109:...

Dein Internetanbieter (ISP) hat dir unbemerkt eine neue IPv4-Adresse zugewiesen. Da deine AWS Security Group (sg-0b8b1e931ba64a86d) wie ein extrem scharfer Türsteher konfiguriert war, der nur Zugriffe von deiner exakten, alten IP (/32) erlaubt, standest du plötzlich auf der Blacklist!

4. Die Entmystifizierung via IMDSv2 und tcpdump

Um auszuschließen, dass der AWS-Netzwerk-Stack oder Linux intern spinnt, hast du den AWS Metadata Service (IMDSv2) via Token-Abfrage vermessen:
Bash

TOKEN=$(curl -X PUT "http://169.254.169.254/latest/api/token" ...)
curl -H "X-aws-ec2-metadata-token: $TOKEN" http://169.254.169.254/latest/meta-data/

Ergebnis: IMDS lieferte alle Daten. Die Instanz war kerngesund. Der anschließende tcpdump-Befehl bestätigte das finale Urteil: Während Port 80-Pakete fröhlich einschlugen, kam auf Port 22 rein gar nichts auf dem Interface an. AWS hat den Traffic gefiltert, noch bevor er das Betriebssystem erreichen konnte. SSH SYN-Pakete erreichten das Interface nicht → Filterung auf AWS Security Group / NACL Ebene wahrscheinlich

## 💡 ERKENNTNIS & LÖSUNG

Das DevSecOps-Paradoxon: "Ich habe meinen Server so unfassbar sicher gegen Angreifer gemacht, dass er jetzt auch absolut sicher vor mir selbst ist." 😄

Am Ende war es keine Geistererscheinung im SSH-Dienst und kein Defekt im Linux-Kernel, sondern die pure, unbestreitbare Präzision der AWS Security Group Inbound Rules in Kombination mit einer dynamischen IP-Änderung deines Routers.

## 🛠️ NOTFALL-PROTOKOLL FÜR DAS NÄCHSTE MAL

Falls dich der AWS-Türsteher mal nicht reinlassen will, ist das hier deine offizielle RNK-Rettungsroute:

## Schritt 1: Aktuelle IP ermitteln

Bash

curl -4 ifconfig.me

## Schritt 2: Security Group via AWS-CLI (oder Handy-Konsole) patchen

Anstatt die Gruppe komplett blind zu öffnen, aktualisierst du die SSH-Regel einfach auf deine neue IP:
Bash

aws ec2 authorize-security-group-ingress \
    --region us-east-1 \
    --group-id sg-0b8b1e931ba64a86d \
    --protocol tcp \
    --port 22 \
    --cidr $(curl -s ifconfig.me)/32

## Schritt 3: Der IPv4-Erzwingungs-Befehl

Falls dein Router versucht, heimlich über IPv6 zu tunneln, zwingst du SSH mit dem Flag -4 auf die erlaubte IPv4-Schiene:
Bash

ssh -4 -i Mojave-Outpost.pem RangerJohnson@98.83.108.196

Logbuch-Eintrag geschlossen. Die Verbindung steht wieder, die Verteidigungsanlagen des Vaults laufen stabil im Hintergrund. Hervorragende Detektivarbeit im System-Unterholz, Ranger! 🫡🛡️🤖🏜️

# 🧷 „Detection Rule für die Zukunft“

## 🧠 PREVENTION (Lesson Learned)

- AWS Security Groups mit /32 sind fragile Single-Point-of-Failure
- Bei dynamischer IP:
  → immer IP vor SSH prüfen
  → oder VPN / bastion / SSM nutzen

Oder noch besser:

👉 „Selbstschutz-Regel“

Vor jeder SG-Änderung:
curl -4 ifconfig.me
