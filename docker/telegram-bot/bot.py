import os
import subprocess
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ConversationHandler, ContextTypes

TOKEN = os.getenv("TELEGRAM_BOT_TOKEN", "PUT_YOUR_TOKEN_HERE")
AUTHORIZED_CHAT_ID = int(os.getenv("AUTHORIZED_CHAT_ID", "123456789"))
SHRED_COMMAND = os.getenv("SHRED_COMMAND", 'powershell -File "C:\\shred_script.ps1"')
WINDOWS_HOST = os.getenv("WINDOWS_HOST", "windows-hostname-or-ip")
WINDOWS_USER = os.getenv("WINDOWS_USER", "admin")
ASK_PASSWORD = 1
SHRED_PASSWORD = os.getenv("SHRED_PASSWORD", "your_secret_password")

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_chat.id != AUTHORIZED_CHAT_ID:
        await update.message.reply_text("❌ Доступ запрещён.")
        return
    await update.message.reply_text("Напиши /shred, чтобы начать уничтожение.")

async def shred(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_chat.id != AUTHORIZED_CHAT_ID:
        await update.message.reply_text("❌ Доступ запрещён.")
        return ConversationHandler.END
    await update.message.reply_text("Введи пароль для подтверждения:")
    return ASK_PASSWORD

async def password_check(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_chat.id != AUTHORIZED_CHAT_ID:
        return ConversationHandler.END
    if update.message.text == SHRED_PASSWORD:
        await update.message.reply_text("✅ Пароль принят. Отдаю команду Windows-шредеру.")
        subprocess.Popen([
            "ssh", f"{WINDOWS_USER}@{WINDOWS_HOST}", SHRED_COMMAND
        ])
        await update.message.reply_text("☠️ Шрединг пошёл.")
    else:
        await update.message.reply_text("❌ Неверный пароль.")
    return ConversationHandler.END

async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("❎ Отменено.")
    return ConversationHandler.END

def main():
    app = ApplicationBuilder().token(TOKEN).build()
    conv = ConversationHandler(
        entry_points=[CommandHandler("shred", shred)],
        states={ASK_PASSWORD: [MessageHandler(filters.TEXT & ~filters.COMMAND, password_check)]},
        fallbacks=[CommandHandler("cancel", cancel)]
    )
    app.add_handler(CommandHandler("start", start))
    app.add_handler(conv)
    app.run_polling()

if __name__ == "__main__":
    main()
