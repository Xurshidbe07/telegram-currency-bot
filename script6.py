from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes

TOKEN = "8944904572:AAFRNA08N1GmCAXL1XytRqHHkvgSKxfCbfA"

# /start bosilganda bot ishga tushadi
async def start(update: Update, context: ContextTypes. DEFAULT_TYPE):
# update.message.text -> bu klientga javob qaytarish metodi
    await update.message.reply_text("Salom! Men tayyorman")

# klientdan text xabar kelganda javob qaytarish metodi
async def xabarga_javob(update: Update, context: ContextTypes. DEFAULT_TYPE):
    kelgan_xat = update.message.text
    # update.message.reply_text -> klientdan kelgan smsni tutib olish
    await update.message.reply_text(f"Siz yozdingiz: {kelgan_xat}")

# hamma yozilgan kod shotta ishga tushadi
if __name__ == "__main__":
    # botni nastroyka qilib ulanish
    app = ApplicationBuilder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    # Klientdan text yoki /stardan boshqa komanda kelsa xabarga_javob metodi
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, xabarga_javob))

    # telegram bot klientdan 24/7 sms kuitb turadi
    app.run_polling()