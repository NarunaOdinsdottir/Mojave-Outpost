import asyncio
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
from telegram.constants import ParseMode
# Wir importieren den neuen Updater und die SIEM-Statusfunktionen
from RNK_Adapter import start_updater, get_siem_status, get_current_report

# --- CONFIGURATION ---
TELEGRAM_TOKEN = "DEIN_TELEGRAM_TOKEN"
CHAT_ID = "DEINE_CHAT_ID"

# Wie oft der Bot prüft, ob das SIEM neue Angriffe in der History aufgezeichnet hat
CHECK_INTERVAL = 5  


# --- BOT COMMANDS (Manuelle Abfrage vom Handy) ---

async def status(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Liefert auf Befehl (/status) den aktuellen SIEM-Zustand ans Handy."""
    siem_status = get_siem_status()
    raw_report = get_current_report()
    
    threat = siem_status["threat_state"]
    metrics = siem_status["metrics"]
    
    # Emoji-Auswahl basierend auf der SIEM-Severity
    severity_emojis = {"LOW": "🟢 LOW", "MEDIUM": "🟡 MEDIUM", "HIGH": "🟠 HIGH", "CRITICAL": "🔴 CRITICAL"}
    sev_display = severity_emojis.get(threat["current_severity"], threat["current_severity"])
    
    health_emoji = "✅" if threat["system_health"] == "HEALTHY" else "⚠️"

    msg = (
        f"🚨 *SekuritronMK2 REPORT*\n"
        f"━━━━━━━━━━━━━━━━━━━━\n"
        f"🛡️ *Threat Severity:* {sev_display}\n"
        f"🏥 *System Health:* {health_emoji} {threat['system_health']}\n"
        f"⏱️ Letztes Update: `{threat['last_updated']}`\n\n"
        f"📊 *SIEM Metriken (Seit Start):*\n"
        f"• Scans verarbeitet: `{metrics['total_scans_performed']}`\n"
        f"• SSH Angriffe blockiert: `{metrics['total_ssh_failed_detected']}`\n"
        f"• SQLi Angriffe blockiert: `{metrics['total_sqli_detected']}`\n"
        f"• Stummgeschaltete Alarme: `{metrics['alerts_muted_by_cooldown']}`\n\n"
    )
    
    # System-Leistungswerte anhängen, falls verfügbar
    if raw_report:
        msg += (
            f"🖥️ *Hardware Auslastung:*\n"
            f"CPU: `{raw_report['cpu']}%` | RAM: `{raw_report['ram']}%` | DISK: `{raw_report['disk']}%`\n\n"
        )
        if raw_report.get("warnings"):
            msg += "⚠️ *Hardware Warnungen:*\n" + "\n".join([f"• {w}" for w in raw_report["warnings"]]) + "\n\n"

    # Die letzten 3 Angriffe aus der bereinigten SIEM-History anzeigen
    history = siem_status["attack_history"]
    if history:
        msg += "🎯 *Letzte SIEM Incidents:*\n"
        for incident in list(history)[-3:]:  # Zeige die letzten 3
            msg += f"• `[{incident['type']}]` von IP: `{incident['source']}` ({incident['severity']})\n"
    else:
        msg += "✅ Keine aktiven Vorfälle in der History."

    # Senden mit MarkdownV2-Unterstützung für saubere Formatierung (z.B. Codeblocks bei IPs)
    await update.message.reply_text(msg, parse_mode=ParseMode.MARKDOWN)


# --- AUTOMATISCHE ALARMIERUNG (Hintergrund-Task) ---

async def alert_monitor_loop(app):
    """
    Überwacht die SIEM Attack History. Sobald ein neuer, ungesehener
    Alarm vom SIEM generiert wird, pusht der Bot ihn aufs Handy.
    """
    # Wir merken uns, wie viele Alarme wir bereits gesendet haben
    last_sent_count = 0
    
    # Kurz warten, bis der SIEM-Adapter warme Daten hat
    await asyncio.sleep(2)
    
    print("📢 SIEM Telegram Push-Notification Loop aktiv...")
    
    while True:
        try:
            siem_status = get_siem_status()
            history = siem_status["attack_history"]
            current_count = len(history)
            
            # Wenn die History gewachsen ist, gibt es neue, verarbeitete Alarme!
            if current_count > last_sent_count:
                # Hole alle Alarme, die seit dem letzten Check dazugekommen sind
                new_alerts = list(history)[last_sent_count:current_count]
                
                for alert in new_alerts:
                    msg = (
                        f"🔥 *🔥 SIEM DETECTED INCIDENT 🔥*\n"
                        f"━━━━━━━━━━━━━━━━━━━━\n"
                        f"🚨 *Typ:* `{alert['type']}`\n"
                        f"🛑 *Severity:* {alert['severity']}\n"
                        f"🌐 *Quelle:* `{alert['source']}`\n"
                        f"📅 *Zeit:* {alert['timestamp']}\n\n"
                        f"📝 *Beschreibung:* \n_{alert['description']}_\n"
                    )
                    await app.bot.send_message(chat_id=CHAT_ID, text=msg, parse_mode=ParseMode.MARKDOWN)
                
                last_sent_count = current_count
                
        except Exception as e:
            print(f"Fehler im Bot Push-Loop: {e}")
            
        # Kurze Pause bis zum nächsten Check der SIEM-History
        await asyncio.sleep(CHECK_INTERVAL)


# --- BOT START SEQUENCE ---

async def main():
    # 1. Starte den SIEM-Core im Hintergrund (deinen neuen adapter.py Updater)
    print("⚙️ Starte SIEM-Core Hintergrund-Updater...")
    start_updater()
    
    # 2. Telegram Bot initialisieren
    app = ApplicationBuilder().token(TELEGRAM_TOKEN).build()
    
    # Befehl /status hinzufügen
    app.add_handler(CommandHandler("status", status))
    
    print("🤖 Securitron SIEM-Bot online...")
    print("📌 Nutze /status auf deinem Handy für eine manuelle Abfrage.")

    # 3. Der Trick: Wir starten den Bot im asynchronen Kontext und fügen 
    # den Alarm-Loop als Hintergrund-Task (create_task) hinzu. Dadurch blockiert er nicht!
    async with app:
        await app.start()
        # Startet den Push-Monitor parallel im Hintergrund
        asyncio.create_task(alert_monitor_loop(app))
        # Hält den Bot am Leben und lauscht auf Befehle von außen
        await app.updater.start_polling()
        
        # Unendlicher Loop, um die Hauptfunktion aktiv zu halten
        while True:
            await asyncio.sleep(3600)

if __name__ == "__main__":
    # Behebt potenzielle Event-Loop-Konflikte auf einigen Plattformen
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        print("\n🤖 Securitron wird heruntergefahren. Auf Wiedersehen!")
