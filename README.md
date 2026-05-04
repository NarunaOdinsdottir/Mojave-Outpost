# Mojave-Outpost
AWS Learing Journey ( Security Edition)


# 🏜️ Mojave Outpost – AWS Learning Journey (Security Edition)

> *„War never changes… but your attack surface does.“*

---

## 📍 Projektübersicht

Willkommen im **Mojave Outpost**.

Dieses Repository dokumentiert meinen Einstieg in AWS mit Fokus auf:

* ☁️ Cloud Fundamentals
* 🔐 Security (IAM, SSH, Hardening)
* 🧠 Denken wie ein Angreifer
* 🛡️ Aufbau eines sicheren Systems

👉 Ziel:
Vom „Cloud User“ → **Security Mindset / DevSecOps**

---

# 🟩 Woche 1 – Fundament legen

## 🎯 Ziel:

Saubere, sichere AWS-Basis

---

## 🔐 IAM & Account Setup

### ⚠️ Root Account

* Wird **nicht verwendet**
* MFA aktiviert

> ❌ Root = God Mode → zu gefährlich für Alltag

---

## 👤 IAM Struktur

Erstellt:

* User: `RangerJohnson`
* Gruppe: `RNK`
* Policy: `AdministratorAccess` (initial)

Später verbessert:

* Rechte vom User entfernt
* Rechte auf Gruppenebene vergeben ✅

---

## 🧠 Learning:

* Root vs IAM User
* Prinzip: **„Wer darf was?“**
* Least Privilege (angerissen)

---

## 🎮 Mini-Mission:

✔️ Login nur noch über IAM User
❌ Root wird ignoriert

---

# 🟨 EC2 – Der erste Server

## 🖥️ Setup

* OS: Ubuntu
* Free Tier Instanz
* SSH Key Pair erstellt

---

## 🔥 Security Group

* Port 22 (SSH) → Zugriff
* Port 80 (HTTP) → Webserver

---

## 🧠 Learning:

* VM = virtueller Computer
* Security Group = **Firewall vor dem Server**

---

## 🎮 Ergebnis:

💥 Server läuft

---

# 🟦 SSH – Zugriff auf den Server

## 🔑 Verbindung

```bash
ssh -i Mojave-Outpost.pem ubuntu@<IP>
```

---

## 💥 Realer Fehler (wichtiger Moment!)

```bash
Permissions 0664 for 'Mojave-Outpost.pem' are too open
```

### 🔧 Fix:

```bash
chmod 400 Mojave-Outpost.pem
```

---

## 🧠 Learning:

* SSH ist **extrem strikt**
* Private Keys dürfen **niemandem sonst zugänglich sein**

> 🔑 Besitz des Keys = Zugriff

---

## 🎮 Ergebnis:

```bash
whoami → ubuntu
```

👉 Zugriff erfolgreich

---

# 🟥 Linux Orientierung

## 🔧 Commands:

```bash
ls
cd
top
uptime
last
```

---

## 🧠 Learning:

* Systemzustand analysieren
* Login-Historie verstehen

---

# 🟪 Woche 1 Abschluss – Reflexion

## ❓ Kernfragen:

* Warum ist Root gefährlich?
* Was macht eine Security Group?
* Warum ist SSH Key sicherer als Passwort?
* Was passiert bei offenen Ports?

---

## 💥 Bonus:

```bash
sudo apt install nginx
```

👉 Webserver läuft öffentlich

---

# 🟡 Woche 2 – Angriffsfläche verstehen

> *„If you can see it… someone else can too.“*

---

## 🔍 Portscan (Recon)

```bash
nmap -sC -sV <IP>
```

---

## 📊 Ergebnis:

* **22/tcp → SSH**
* **80/tcp → HTTP (nginx)**

---

## 🧠 Learning:

* Ports = Zugangspunkte
* Jeder offene Port = potenzieller Angriffspunkt

---

## ☠️ Risiko:

* Port 22 = Hauptziel für Brute Force
* Viele offene Ports = große Angriffsfläche

---

# 🛡️ Security Groups (Level Up)

## 🔐 Aktuelle Konfiguration:

### Inbound:

* SSH → nur eigene IP ✅
* HTTP → öffentlich ✅

### Outbound:

* alles erlaubt (Standard)

---

## 🧠 Learning:

> Security Group = **erste Verteidigungslinie**

---

## 🎮 Mini-Mission:

* SSH komplett sperren
* Zugriff wiederherstellen

👉 Realitätstest bestanden

---

# 🟥 Server Hardening

## 🔧 System Updates

```bash
sudo apt update && sudo apt upgrade -y
```

---

## 🔐 SSH Hardening

```bash
PermitRootLogin no
PasswordAuthentication no
```

---

## 🧠 Learning:

* Kein Passwort-Login
* Nur Key-basierter Zugriff

---

## 🔥 Firewall (UFW)

```bash
sudo ufw enable
sudo ufw allow OpenSSH
```

---

## 🧱 Defense Layers

* Security Group (extern)
* UFW (intern)
* SSH Config (Zugriff)

---

# 👤 Benutzer-Setup (Security Upgrade)

## Neuer User:

```bash
sudo adduser RangerJohnson
sudo usermod -aG sudo RangerJohnson
```

---

## SSH Zugriff vorbereiten

```bash
mkdir -p ~/.ssh
chmod 700 ~/.ssh
chmod 600 authorized_keys
```

---

## 🧠 Prinzip:

> 🔐 Schlüssel + Passwort = zusätzlicher Schutzlayer

---

## 🔥 Optional:

```bash
sudo usermod -L ubuntu
```

👉 Default-User deaktivieren

---

# 📊 Monitoring & Logs

## 🔍 Logs analysieren:

```bash
cat /var/log/auth.log
```

---

## 🧠 Erkenntnis:

* Erste Bot-Aktivität sichtbar
* Internet scannt **immer**

---

# ⚙️ Python Problem (Real World Issue)

## ❌ Fehler:

```bash
ModuleNotFoundError: psutil
```

---

## 💥 Ursache:

PEP 668 → System-Python geschützt

---

## ✅ Lösung:

```bash
sudo apt install python3-venv
python3 -m venv venv
source venv/bin/activate
pip install psutil
```

---

## 🧠 Learning:

* Virtual Environments = Standard
* System-Python nicht verändern

---

# 🧠 Security Erkenntnisse

## 🔑 SSH

* Key-basierter Zugriff aktiv
* Passwort deaktiviert

---

## 🛡️ Defense

* Angriffsfläche reduziert
* Zugriff eingeschränkt
* Monitoring aktiv

---

## ☠️ Realität

* Bots scannen permanent
* Logs zeigen erste Aktivitäten

---

# 🏜️ Mojave Outpost Status

| System          | Status       |
| --------------- | ------------ |
| IAM             | ✅ sauber     |
| EC2             | ✅ aktiv      |
| SSH             | ✅ gehärtet   |
| Firewall        | ✅ aktiv      |
| User Management | ✅ verbessert |
| Monitoring      | 🟡 im Aufbau |

---

# 🚀 Nächste Schritte

* 🔍 Intrusion Detection
* 📊 Monitoring Dashboard (Vault Watcher)
* 🔐 IAM Feingranularität
* 🧪 Angriffssimulationen
* ☁️ Infrastructure as Code

---

# 💬 Abschluss

> *„The Mojave taught me one thing…
> Security isn’t optional.“*

---

**Status:** 🟢 Aktiv im Aufbau
**Codename:** Mojave Outpost
**Fraktion:** RNK (Ranger Nane Kommando 😄)
