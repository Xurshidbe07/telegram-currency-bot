
from telegram import Update, ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters, CallbackQueryHandler

TOKEN = "8975814485:AAGTJGNCQ6YaIR61zBUyMhU07iJi6JqT4po"

USER_STEP = ""
USER_NAME = ""
USER_SURNAME = ""
USER_FATHER_NAME = ""

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    tashqi_knopka = ReplyKeyboardMarkup( keyboard=[
        [
            KeyboardButton(text="📝Ro'yxatdan o'tish"),
            KeyboardButton(text="ℹ️Ma'lumot")
        ],
        [
            KeyboardButton(text="❓Yordam")
        ]
    ], resize_keyboard=True)

    await update.message.reply_text("Assalom aleykum botimizga xush kelibsiz", reply_markup=tashqi_knopka)

async def main(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text
    global USER_STEP

    if text == "📝Ro'yxatdan o'tish":
        ichki_knopka = InlineKeyboardMarkup([
            [
                InlineKeyboardButton("Ismingizni kiriting tugmasi", callback_data="register"),
                InlineKeyboardButton("Familyangizni kirirtish tugmasi", callback_data="quick")
            ],
            [
                InlineKeyboardButton("Qo'shimcha ma'lumot", callback_data="help")
            ]
        ])
        await update.message.reply_text("Ro'yxatdan otish", reply_markup=ichki_knopka)
    elif text == "ℹ️Ma'lumot":
        await update.message.reply_text("Siz Ma'lumot knopkasini bosdingiz ")
    elif text == "❓Yordam":
        await update.message.reply_text("Uzr sizga yordam bera olmaymiz")
    elif USER_STEP == "name":
        USER_STEP = text
        await update.message.reply_text(f"Ismingiz saqlandi {USER_NAME}")
    elif USER_STEP == "surname":
        USER_STEP = text
        await update.message.reply_text(f"Familyangiz saqlandi {USER_SURNAME}")

async def inline_button_click(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    global USER_STEP
    if query.data == "register":
        USER_STEP = "name"
        await query.message.reply_text("Iltimos ismingizni kiriting ")
    elif query.data == "quick":
        USER_STEP = "surname"
        await query.message.reply_text("Iltimos familyangizni kiririting ")
    elif query.data == "help":
        await query.message.reply_text(f"Sizni malumotlariz: \n"
            f"{USER_NAME} {USER_SURNAME}"
        )

if __name__ == '__main__':
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, main))
    app.add_handler(CallbackQueryHandler(inline_button_click))
    print("Bot ishga tushdi")

    app.run_polling()