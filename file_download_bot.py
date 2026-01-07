import os
import requests
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters

BOT_TOKEN = "8577319519:AAHnaebOYVy_TdgJW1bJ73hma-5UG4wfG0E"

DOWNLOAD_DIR = "downloads"
os.makedirs(DOWNLOAD_DIR, exist_ok=True)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "👋 Hello!\nSend me any direct download link and I will download the file for you."
    )

async def handle_link(update: Update, context: ContextTypes.DEFAULT_TYPE):
    url = update.message.text.strip()
    try:
        await update.message.reply_text("⏳ Downloading...")
        r = requests.get(url, stream=True, timeout=60)
        r.raise_for_status()

        filename = url.split("/")[-1] or "file"
        path = os.path.join(DOWNLOAD_DIR, filename)

        with open(path, "wb") as f:
            for chunk in r.iter_content(10240):
                if chunk:
                    f.write(chunk)

        await update.message.reply_document(document=open(path, "rb"))
        os.remove(path)

    except Exception as e:
        await update.message.reply_text(f"❌ Error: {e}")

def main():
    app = ApplicationBuilder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_link))
    app.run_polling()

if __name__ == "__main__":
    main()
