from telegram import ReplyKeyboardMarkup, KeyboardButton, Update
from telegram.ext import CommandHandler, ApplicationBuilder, MessageHandler, filters, CallbackQueryHandler, ContextTypes

TOKEN = "8944904572:AAFRNA08N1GmCAXL1XytRqHHkvgSKxfCbfA"

USER_STEP = ""
USER_NAME = ""
USER_SURNAME = ""
USER_FATHER_NAME = ""

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) :
    global USER_STEP
    USER_STEP = "menu"

    knopka = ReplyKeyboardMarkup(
        keyboard=[
        [KeyboardButton(text = "Ro'yxatdan o'tish")],
        [KeyboardButton(text = "Ma'lumot")],

    ], resize_keyboard=True )

    await update.message.reply_text(("assalomu aleykum"), reply_markup=knopka)

async def main(update: Update, context: ContextTypes.DEFAULT_TYPE) :
    global USER_STEP, USER_NAME, USER_SURNAME, USER_FATHER_NAME
    text = update.message.text

    if USER_STEP == "menu" :
        if text == "Ro'yxatdan o'tish" :
            await update.message.reply_text("")

if __name__ == '__main__':
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))

    print("Bot ishga tushdi")

    app.run_polling()

