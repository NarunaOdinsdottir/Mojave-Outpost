import asyncio
from telegram import Update
from telegram import Bot  
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
from RNK_Adapter import get_current_report
from RNK_Monitor import get_report
import time
import os

CHECK_INTERVAL = 300  # alle 5 Minuten

# Telegram Config
TELEGRAM_TOKEN = ""
CHAT_ID = ""

async def send_alert(bot_instance, report):
    msg = f"📊 Vault-OS Alert [{report['timestamp']}]\n"
    msg += f"CPU: {report['cpu']:.1f}% | RAM: {report['ram']:.1f}% | DISK: {report['disk']:.1f}%\n"

    if report["warnings"]:
        msg += "\n🚨 WARNUNGEN:\n"
        for w in report["warnings"]:
            msg += f"{w}\n"
    else:
        msg += "\n✅ Alles stabil.\n"

    if report["suspicious"]:
        msg += "\n⚠️ Verdächtige Prozesse:\n"
        msg += "\n".join(report["suspicious"]) + "\n"

    msg += f"\n👤 Letzter Login:\n{report['last_login']}\n"

    await bot_instance.send_message(chat_id=CHAT_ID, text=msg)

async def status(update: Update, context: ContextTypes.DEFAULT_TYPE):
    report = get_report()
    
    msg = (
        f"🚨 **VAULT STATUS REPORT**\n"
        f"━━━━━━━━━━━━━━━━━━━━\n"
        f"📊 **Threat Level:** {report['threat_level']}\n"
        f"⏱️ Zeit: {report['timestamp']}\n\n"
        f"👤 **SSH Status:**\n"
        f"Failed Logins: {report['failed_logins_count']}\n"
        f"Letzte verdächtige IP: `{report['last_failed_ip']}`\n\n"
        f"🖥️ **System:**\n"
        f"CPU: {report['cpu']}% | RAM: {report['ram']}%"
    )

    if report["warnings"]:
        msg += "\n\n⚠️ **WARNUNGEN:**\n" + "\n".join(report["warnings"])
    
    await update.message.reply_text(msg, parse_mode='Markdown')

# 🔹 Hintergrund-Überwachung
async def monitor_loop(app):
    while True:
        report = get_report()

        if report["warnings"]:
            msg = "🚨 VAULT ALERT 🚨\n"
            for w in report["warnings"]:
                msg += f"{w}\n"

            await app.bot.send_message(chat_id=CHAT_ID, text=msg)

        await asyncio.sleep(300)  # alle 5 Minuten

# 🔹 Start
async def main():
    app = ApplicationBuilder().token(TELEGRAM_TOKEN).build()
    app.add_handler(CommandHandler("status", status))
    
    print("Status Command empfangen!")  # ← Debug
    print("🤖 Securitron online...")  # ← MUSS erscheinen!

    async with app:
        await app.start()
        await monitor_loop(app)

if __name__ == "__main__":
    asyncio.run(main())
