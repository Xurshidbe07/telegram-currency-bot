
from telegram import Update, ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters, CallbackQueryHandler

TOKEN = "8975814485:AAGTJGNCQ6YaIR61zBUyMhU07iJi6JqT4po"

USER_STEP = ""
USER_NAME = ""
USER_SURNAME = ""
USER_FATHER_NAME = ""

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    global USER_STEP
    USER_STEP = "menu"

    knopka = ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="Ro'yxatdan o'tish")],
            [KeyboardButton(text="Ma'lumot")],
        ], resize_keyboard=True
    )

    await update.message.reply_text(text="Assalaomu aleykum botimizga xush kelibsiz", reply_markup=knopka)

async def main(update: Update, context: ContextTypes.DEFAULT_TYPE):
    global USER_STEP, USER_NAME, USER_SURNAME, USER_FATHER_NAME

    text = update.message.text

    if USER_STEP == "menu" :
        if text == "Ro'yxatdan o'tish" :
            await update.message.reply_text("Iltimos ismingizni kiriting")
            USER_STEP = "name"
        elif text == "Ma'lumot" :
            await update.message.reply_text("Bu sizni malumot saqlaydigan botingiz")
        else:
            await update.message.reply_text("Iltimos pastdagi knopkalardan foydalaning")
    elif USER_STEP == "name" :
        USER_NAME = text
        USER_STEP = "surname"
        await update.message.reply_text("Iltimos familyangizni kiriting")
    elif USER_STEP == "surname" :
        USER_SURNAME = text
        await update.message.reply_text("Iltimos otchestvezi kiriting ")
        USER_STEP = "father_name"
    elif USER_STEP == "father_name" :
        USER_FATHER_NAME = text
        await update.message.reply_text(
            f"Sizni malumotlariz: \n"
            f"{USER_NAME} {USER_SURNAME} {USER_FATHER_NAME}"
        )

if __name__ == '__main__':
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, main))
    print("Bot ishga tushdi")
    app.run_polling()
