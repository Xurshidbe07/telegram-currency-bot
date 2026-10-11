from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup, KeyboardButton
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    MessageHandler,
    CallbackQueryHandler,
    ContextTypes,
    filters
)

TOKEN = "8975814485:AAGTJGNCQ6YaIR61zBUyMhU07iJi6JqT4po"

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    tashqi_knopka = ReplyKeyboardMarkup( keyboard=[
        [
            KeyboardButton(text="📞 Telefon raqamni yuborish", request_contact=True),
            KeyboardButton(text="Ism familya yuborish")
        ]
    ], resize_keyboard=True)

    await update.message.reply_text("mana knopkalar", reply_markup=tashqi_knopka)

async def contact_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    contact = update.message.contact
    phone_number = contact.phone_number
    first_name = contact.first_name

    await update.message.reply_text(
        f"Rahmat, {first_name}! Sizning telefon raqamingiz qabul qilindi: {phone_number}"
    )

if __name__ == '__main__':
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.CONTACT, contact_handler))
    print("Bot ishga tushdi")
    app.run_polling()