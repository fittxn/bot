from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes
import subprocess, os

BOT_TOKEN = "8188932777:AAGB6ghqC4B7llo5frUecLVfgF54tbgjVM0"

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("سلام علی! لینک Spotify یا SoundCloud بفرست 🎧")

async def handle(update: Update, context: ContextTypes.DEFAULT_TYPE):
    msg = update.message.text
    chat_id = update.effective_chat.id

    if "spotify.com" in msg:
        await update.message.reply_text("🎵 در حال دانلود از اسپاتیفای...")
        subprocess.run(f"spotdl {msg} --output song.mp3", shell=True)
        await context.bot.send_audio(chat_id=chat_id, audio=open("song.mp3", "rb"))
        os.remove("song.mp3")

    elif "soundcloud.com" in msg:
        await update.message.reply_text("🎶 در حال دانلود از ساندکلود...")
        subprocess.run(f"scdl -l {msg} -o .", shell=True)
        for f in os.listdir("."):
            if f.endswith(".mp3"):
                await context.bot.send_audio(chat_id=chat_id, audio=open(f, "rb"))
                os.remove(f)
    else:
        await update.message.reply_text("لینک معتبر بفرست 🙏")

app = ApplicationBuilder().token(BOT_TOKEN).build()
app.add_handler(CommandHandler("start", start))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle))
app.run_polling()
