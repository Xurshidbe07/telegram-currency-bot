
from telegram import Update
from telegram.ext import CommandHandler, MessageHandler, ContextTypes, filters, ApplicationBuilder

TOKEN = "8944904572:AAFRNA08N1GmCAXL1XytRqHHkvgSKxfCbfA"

NAME, SURNAME, FATHERS_NAME = range(3)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data.clear()
    context.user_data["step"] = "name"
    await update.message.reply_text("iltimos ismingizni kiriting: ")

async def message(update: Update, context: ContextTypes.DEFAULT_TYPE):

    if context.user_data.get("step") == "name":
        context.user_data["step"] = "surname"
        global NAME
        NAME = update.message.text
        await update.message.reply_text("iltimos familyangizni kiriting: ")

    elif context.user_data.get("step") == "surname":
        context.user_data["step"] = "father_name"
        global SURNAME
        SURNAME = update.message.text
        await update.message.reply_text("iltimos otchestezi kiriting: ")

    elif context.user_data.get("step") == "fathers_name":
        global FATHERS_NAME
        FATHERS_NAME = update.message.text

        await update.message.reply_text(
            f"Sizning ism familiyangiz:\n"
            f"{context.user_data['name']} {context.user_data['surname']} {context.user_data['fathers_name']}"
        )
        context.user_data.clear()

if __name__ == "__main__":
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, message ))
    app.run_polling()
