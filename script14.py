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

    await update.message.reply_text("mana knopkalar", reply_markup=tashqi_knopka)

async def main(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text
    if text == "📝Ro'yxatdan o'tish":
        ichki_knopka = InlineKeyboardMarkup([
            [
                InlineKeyboardButton("Ism kiritish tugmasi", callback_data="register"),
                InlineKeyboardButton("Familya kiritish tugmasi", callback_data="quick")
            ],
            [
                InlineKeyboardButton("❓Yordam", callback_data="help")
            ]
        ])
        await update.message.reply_text("mana inline knopkalar", reply_markup=ichki_knopka)
    elif text == "ℹ️Ma'lumot":
        await update.message.reply_text("Siz Ma'lumot knopkasini bosdingiz ")
    elif text == "❓Yordam":
        await update.message.reply_text("Uzr sizga yordam bera olmaymiz")
    else:
        await update.message.reply_text("iltimos knopkalardan foydalaning")

async def inline_button_click(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    if query.data == "register":
        await query.message.reply_text("Iltimos ismingizni kiriting ")

    elif query.data == "quick":
        await query.message.reply_text("Iltimos familyangizni kiriting")
    elif query.data == "help":
        await query.message.reply_text("Uzr sizga yordam bera olmaymiz")

if __name__ == '__main__':
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, main))
    app.add_handler(CallbackQueryHandler(inline_button_click))
    print("Bot ishga tushdi")

    app.run_polling()