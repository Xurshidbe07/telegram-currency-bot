from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup, KeyboardButton
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    MessageHandler,
    CallbackQueryHandler,
    ContextTypes,
    filters
)
import psycopg

conn = psycopg.connect(
    dbname="telegram_bot",
    user="postgres",
    password="qwert001",
    host="localhost",
    port="5432"
)

TOKEN = "8975814485:AAGTJGNCQ6YaIR61zBUyMhU07iJi6JqT4po"

USD1, USD2 = 12000, 12200
EUR1, EUR2 = 14000, 13700

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data.clear()
    context.user_data["step"] = "name"
    await update.message.reply_text("Assalomu alaykum! Iltimos, ism va familiyangizni kiriting:")

async def registration(update: Update, context: ContextTypes.DEFAULT_TYPE):
    step = context.user_data.get("step")
    message = update.message.text

    if step == "name":
        context.user_data["name"] = message
        context.user_data["step"] = "phone"
        keyboard0 = ReplyKeyboardMarkup([
            [KeyboardButton("📱 Telefon raqam yuborish", request_contact=True)]
        ], resize_keyboard=True)
        await update.message.reply_text("📱 Telefon raqamingizni yuboring:", reply_markup=keyboard0)

    elif step == "phone":
        if update.message.contact:
            phone = update.message.contact.phone_number
            context.user_data["phone"] = phone
            context.user_data["step"] = "email"
            await update.message.reply_text("Iltimos, elektron pochtangizni kiriting (Masalan: example@gmail.com):")
        else:
            await update.message.reply_text("❌ Iltimos, pastdagi '📱 Telefon raqam yuborish' tugmasini bosing.")

    elif step == "email":
        if "@" not in message or "." not in message:
            await update.message.reply_text("❌ Email noto'g'ri formatda.\nMasalan: example@gmail.com")
            return

        context.user_data["email"] = message
        context.user_data["step"] = "confirm"

        keyboard = InlineKeyboardMarkup([
            [
                InlineKeyboardButton("✅ Tasdiqlash", callback_data="confirm"),
                InlineKeyboardButton("❌ Bekor qilish", callback_data="cancel")
            ]
        ])
        await update.message.reply_text(
            f"📋 Ma'lumotlaringiz:\n\n"
            f"👤 Ism: {context.user_data['name']}\n"
            f"📱 Telefon: {context.user_data['phone']}\n"
            f"📧 Email: {context.user_data['email']}\n\n"
            f"Ma'lumotlarni tasdiqlaysizmi?",
            reply_markup=keyboard
        )

async def confirm_registration(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    if query.data == "confirm":
        with conn.cursor() as cur:
            cur.execute(
                """
                INSERT INTO users (telegram_id, name, phone, email)
                VALUES (%s, %s, %s, %s)
                ON CONFLICT (telegram_id)
                DO UPDATE SET
                name = EXCLUDED.name,
                phone = EXCLUDED.phone,
                email = EXCLUDED.email
                """,
                (update.effective_user.id, context.user_data["name"],
                 context.user_data["phone"], context.user_data["email"])
            )

        conn.commit()
        context.user_data["registered"] = True
        context.user_data.pop("step", None)

        keyboard2 = ReplyKeyboardMarkup([
            [
                KeyboardButton("🇺🇸 USD kursini ko'rish"),
                KeyboardButton("🇪🇺 EUR kursini ko'rish")
            ]
        ], resize_keyboard=True)

        await query.message.reply_text(
            f"✅ Ro'yxatdan o'tish muvaffaqiyatli yakunlandi!\n"
            f"Xush kelibsiz, {context.user_data['name']}!",
            reply_markup=keyboard2
        )
    elif query.data == "cancel":
        context.user_data.clear()
        await query.message.reply_text("❌ Ro'yxatdan o'tish bekor qilindi. Qaytadan boshlash uchun /start bosing.")


async def hisoblash(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text or ""

    if text == "🇺🇸 USD kursini ko'rish":
        keyboard = InlineKeyboardMarkup([
            [InlineKeyboardButton("🇺🇸 USD → 🇺🇿 UZS", callback_data="usd_uzs")],
            [InlineKeyboardButton("🇺🇿 UZS → 🇺🇸 USD", callback_data="uzs_usd")]
        ])
        await update.message.reply_text(
            f"🇺🇸 USD kursi:\nOldingi: {USD1} UZS\nHozirgi: {USD2} UZS",
            reply_markup=keyboard
        )
        return

    elif text == "🇪🇺 EUR kursini ko'rish":
        keyboard = InlineKeyboardMarkup([
            [InlineKeyboardButton("🇪🇺 EUR → 🇺🇿 UZS", callback_data="eur_uzs")],
            [InlineKeyboardButton("🇺🇿 UZS → 🇪🇺 EUR", callback_data="uzs_eur")]
        ])
        await update.message.reply_text(
            f"🇪🇺 EUR kursi:\nOldingi: {EUR1} UZS\nHozirgi: {EUR2} UZS",
            reply_markup=keyboard
        )
        return

    operation = context.user_data.get("operatsiya")

    if not operation:
        return
    summa = float(text)

    if operation == "usd_uzs":
        natija = summa * USD2
        await update.message.reply_text(f"🇺🇸 {summa} USD = 🇺🇿 {natija:,.2f} UZS")
    elif operation == "eur_uzs":
        natija = summa * EUR2
        await update.message.reply_text(f"🇪🇺 {summa} EUR = 🇺🇿 {natija:,.2f} UZS")
    elif operation == "uzs_usd":
        natija = summa / USD2
        await update.message.reply_text(f"🇺🇿 {summa} UZS = 🇺🇸 {natija:,.2f} USD")
    elif operation == "uzs_eur":
        natija = summa / EUR2
        await update.message.reply_text(f"🇺🇿 {summa} UZS = 🇪🇺 {natija:,.2f} EUR")

    context.user_data.pop("operatsiya", None)

async def button(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    if query.data == "usd_uzs":
        context.user_data["operatsiya"] = "usd_uzs"
        await query.message.reply_text("🇺🇸 USD miqdorini kiriting:")
    elif query.data == "eur_uzs":
        context.user_data["operatsiya"] = "eur_uzs"
        await query.message.reply_text("🇪🇺 EUR miqdorini kiriting:")
    elif query.data == "uzs_usd":
        context.user_data["operatsiya"] = "uzs_usd"
        await query.message.reply_text("🇺🇿 UZS miqdorini kiriting:")
    elif query.data == "uzs_eur":
        context.user_data["operatsiya"] = "uzs_eur"
        await query.message.reply_text("🇺🇿 UZS miqdorini kiriting:")

if __name__ == '__main__':
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(confirm_registration, pattern="^(confirm|cancel)$"))
    app.add_handler(CallbackQueryHandler(button))
    app.add_handler(MessageHandler(filters.CONTACT, registration))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, registration), group=1)
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, hisoblash), group=2)

    print("Bot ishga tushdi...")
    app.run_polling()