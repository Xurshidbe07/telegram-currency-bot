
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    MessageHandler,
    CallbackQueryHandler,
    ContextTypes,
    filters
)

TOKEN = "8975814485:AAGTJGNCQ6YaIR61zBUyMhU07iJi6JqT4po"

USD = 12500
EUR = 14500

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data.clear()

    keyboard = [
        [
            InlineKeyboardButton("🇺🇸 USD → 🇺🇿 UZS", callback_data="usd_uzs"),
            InlineKeyboardButton("🇪🇺 EUR → 🇺🇿 UZS", callback_data="eur_uzs")
        ],
        [
            InlineKeyboardButton("🇺🇿 UZS → 🇺🇸 USD", callback_data="uzs_usd"),
            InlineKeyboardButton("🇺🇿 UZS → 🇪🇺 EUR", callback_data="uzs_eur")
        ]
    ]

    reply_markup = InlineKeyboardMarkup(keyboard)

    await update.message.reply_text(
        "💱 Valyuta servisiga xush kelibsiz!\n\n"
        "Qaysi valyutani almashtirmoqchisiz?",
        reply_markup=reply_markup
    )


# Inline knopka bosilganda
async def button(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query

    await query.answer()

    if query.data == "usd_uzs":
        context.user_data["operation"] = "usd_uzs"

        await query.message.reply_text(
            "🇺🇸 USD miqdorini kiriting:"
        )

    elif query.data == "eur_uzs":
        context.user_data["operation"] = "eur_uzs"

        await query.message.reply_text(
            "🇪🇺 EUR miqdorini kiriting:"
        )

    elif query.data == "uzs_usd":
        context.user_data["operation"] = "uzs_usd"

        await query.message.reply_text(
            "🇺🇿 UZS miqdorini kiriting:"
        )

    elif query.data == "uzs_eur":
        context.user_data["operation"] = "uzs_eur"

        await query.message.reply_text(
            "🇺🇿 UZS miqdorini kiriting:"
        )


# Son kiritilganda
async def calculate(update: Update, context: ContextTypes.DEFAULT_TYPE):

    if "operation" not in context.user_data:
        await update.message.reply_text(
            "Avval /start buyrug'ini bosing."
        )
        return

    try:
        summa = float(update.message.text)

    except ValueError:
        await update.message.reply_text(
            "❌ Iltimos, faqat son kiriting.\n"
            "Masalan: 100"
        )
        return

    operation = context.user_data["operation"]

    # USD → UZS
    if operation == "usd_uzs":

        natija = summa * USD

        await update.message.reply_text(
            f"🇺🇸 {summa} USD\n"
            f"🇺🇿 {natija:,.0f} UZS"
        )

    # EUR → UZS
    elif operation == "eur_uzs":

        natija = summa * EUR

        await update.message.reply_text(
            f"🇪🇺 {summa} EUR\n"
            f"🇺🇿 {natija:,.0f} UZS"
        )

    # UZS → USD
    elif operation == "uzs_usd":

        natija = summa / USD

        await update.message.reply_text(
            f"🇺🇿 {summa:,.0f} UZS\n"
            f"🇺🇸 {natija:.2f} USD"
        )

    # UZS → EUR
    elif operation == "uzs_eur":

        natija = summa / EUR

        await update.message.reply_text(
            f"🇺🇿 {summa:,.0f} UZS\n"
            f"🇪🇺 {natija:.2f} EUR"
        )

    context.user_data.clear()

if __name__ == '__main__':
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(button))
    app.add_handler(
        MessageHandler(filters.TEXT & ~filters.COMMAND, calculate)
    )
    print("Bot ishga tushdi")
    app.run_polling()
