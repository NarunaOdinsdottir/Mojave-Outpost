import asyncio
import requests
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
from telegram.constants import ParseMode

# --- KONFIGURATION ---
TELEGRAM_TOKEN = "DEIN_BOT_TOKEN_HIER"
CHAT_ID = 123456789  
CHECK_INTERVAL = 5   

API_URL = "http://127.0.0.1:8000/api/v1/status"

def fetch_siem_state_from_api():
    """Fragt den aktuellen Zustand per HTTP-Schnittstelle ab."""
    try:
        response = requests.get(API_URL, timeout=2)
        if response.status_code == 200:
            return response.json()
    except requests.exceptions.RequestException:
        # API-Server temporär offline oder startet gerade noch
        return None
    return None


# --- BOT COMMANDS ---

async def status(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Holt den Status live über die API-Schnittstelle."""
    data = fetch_siem_state_from_api()
    
    if not data:
        await update.message.reply_text("❌ SIEM-API antwortet nicht. Läuft die RNK_Adapter.py?")
        return
        
    threat = data["threat_state"]
    metrics = data["metrics"]
    stats = data.get("system_stats", {"cpu": 0, "ram": 0, "disk": 0})
    warnings = data.get("latest_raw_warnings", [])
    
    severity_emojis = {"LOW": "🟢 LOW", "MEDIUM": "🟡 MEDIUM", "HIGH": "🟠 HIGH", "CRITICAL": "🔴 CRITICAL"}
    sev_display = severity_emojis.get(threat["current_severity"], threat["current_severity"])
    health_emoji = "✅" if threat["system_health"] == "HEALTHY" else "⚠️"

    msg = (
        f"🚨 <b>Victors Server REPORT</b>\n"
        f"━━━━━━━━━━━━━━━━━━━━\n"
        f"🛡️ <b>Threat Severity:</b> {sev_display}\n"
        f"🏥 <b>System Health:</b> {health_emoji} {threat['system_health']}\n"
        f"⏱️ Letztes Update: <code>{threat['last_updated']}</code>\n\n"
        f"🖥️ <b>Hardware Auslastung:</b>\n"
        f"CPU: <code>{stats['cpu']}%</code> | RAM: <code>{stats['ram']}%</code> | DISK: <code>{stats['disk']}%</code>\n\n"
    )
    
    if warnings:
        msg += "⚠️ <b>System-Warnungen:</b>\n" + "\n".join([f"• {w}" for w in warnings]) + "\n\n"
    else:
        msg += "✅ Hardware-Status im grünen Bereich.\n\n"

    msg += (
        f"📊 <b>SIEM Metriken:</b>\n"
        f"• Scans verarbeitet: <code>{metrics['total_scans_performed']}</code>\n"
        f"• SSH Angriffe blockiert: <code>{metrics['total_ssh_failed_detected']}</code>\n"
        f"• SQLi Angriffe blockiert: <code>{metrics['total_sqli_detected']}</code>\n"
        f"• Stummgeschaltete Alarme: <code>{metrics['alerts_muted_by_cooldown']}</code>\n\n"
    )
    
    history = data.get("attack_history", [])
    if history:
        msg += "🎯 <b>Letzte SIEM Incidents:</b>\n"
        for incident in list(history)[-3:]:  
            msg += f"• <code>[{incident['type']}]</code> von IP: <code>{incident['source']}</code> ({incident['severity']})\n"
    else:
        msg += "✅ Howdy Partner! Keine aktiven Vorfälle in der History. Die Vault ist gesichert."

    await update.message.reply_text(msg, parse_mode=ParseMode.HTML)


# --- AUTOMATISCHE ALARMIERUNG (Hintergrund-Task) ---

async def alert_monitor_loop(app):
    """Überwacht die API auf neue, ungesehene Angriffe."""
    print("📢 Securitron API-Push Loop aktiv...")
    
    # Spam-Schutz beim Initialisieren abrufen
    initial_data = fetch_siem_state_from_api()
    if initial_data and "attack_history" in initial_data:
        last_sent_count = len(initial_data["attack_history"])
        print(f"ℹ️ Bot mit {last_sent_count} bekannten Vorfällen synchronisiert.")
    else:
        last_sent_count = 0
    
    await asyncio.sleep(2)
    
    while True:
        try:
            data = fetch_siem_state_from_api()
            if data and "attack_history" in data:
                history = data["attack_history"]
                current_count = len(history)
                
                if current_count > last_sent_count:
                    new_alerts = history[last_sent_count:current_count]
                    
                    for alert in new_alerts:
                        msg = (
                            f"🔥 <b>Vault-Tec DETECTED INCIDENT (API)</b> 🔥\n"
                            f"━━━━━━━━━━━━━━━━━━━━\n"
                            f"🚨 <b>Typ:</b> <code>{alert['type']}</code>\n"
                            f"🛑 <b>Severity:</b> {alert['severity']}\n"
                            f"🌐 <b>Quelle:</b> <code>{alert['source']}</code>\n"
                            f"📅 <b>Zeit:</b> {alert['timestamp']}\n\n"
                            f"📝 <b>Beschreibung:</b> \n<i>{alert['description']}</i>"
                        )
                        await app.bot.send_message(chat_id=CHAT_ID, text=msg, parse_mode=ParseMode.HTML)
                    
                    last_sent_count = current_count
                    
        except Exception as e:
            print(f"Fehler im API-Bot Loop: {e}")
            
        await asyncio.sleep(CHECK_INTERVAL)


# --- BOT START SEQUENCE ---

async def main():
    print("🤖 Securitron SIEM-Bot online (API Client-Modus)...")
    app = ApplicationBuilder().token(TELEGRAM_TOKEN).build()
    app.add_handler(CommandHandler("status", status))
    
    async with app:
        await app.start()
        asyncio.create_task(alert_monitor_loop(app))
        await app.updater.start_polling()
        
        while True:
            await asyncio.sleep(3600)

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        print("\n🤖 Securitron wird heruntergefahren.")
