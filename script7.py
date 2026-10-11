from telegram import Update
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    MessageHandler,
    ContextTypes,
    filters,
)

TOKEN = "8944904572:AAFRNA08N1GmCAXL1XytRqHHkvgSKxfCbfA"

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data.clear()
    context.user_data["step"] = "name"
    await update.message.reply_text("Ismingizni kiriting:")

async def message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text

    if context.user_data.get("step") == "name":
        context.user_data["name"] = text
        context.user_data["step"] = "surname"
        await update.message.reply_text("Familiyangizni kiriting:")

    elif context.user_data.get("step") == "surname":
        context.user_data["surname"] = text
        context.user_data["step"] = "father_name"
        await update.message.reply_text("Otangizni ismini kiriting:")

    elif context.user_data.get("step") == "father_name":
        context.user_data["father_name"] = text


        await update.message.reply_text(
            f"Sizning ism familiyangiz:\n"
            f"{context.user_data['name']} {context.user_data['surname']} {context.user_data['father_name']}"
        )


app = ApplicationBuilder().token(TOKEN).build()

app.add_handler(CommandHandler("start", start))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, message))

app.run_polling()