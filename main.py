from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    CallbackQueryHandler,
    ContextTypes
)

TOKEN = "8754551838:AAE-8Du0lEB0e_rhou0F7Mo7dUZNcRgLsMw"
CHANNEL = "@t.me/tg263e"


# ✅ Проверка подписки
async def is_subscribed(user_id, bot):
    member = await bot.get_chat_member(chat_id=CHANNEL, user_id=user_id)
    return member.status in ["member", "administrator", "creator"]


# 🚀 Старт
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id

    if not await is_subscribed(user_id, context.bot):
        keyboard = [
            [InlineKeyboardButton("📢 Подписаться", url=f"https://t.me/{CHANNEL[1:]}")],
            [InlineKeyboardButton("✅ Проверить", callback_data="check_sub")]
        ]

        await update.message.reply_text(
            "❗ Подпишись на канал, чтобы пользоваться ботом",
            reply_markup=InlineKeyboardMarkup(keyboard)
        )
        return

    keyboard = [
        [InlineKeyboardButton("🛍 Магазин", callback_data="shop")],
        [InlineKeyboardButton("ℹ️ О нас", callback_data="about")]
    ]

    await update.message.reply_text(
        "Добро пожаловать в магазин!",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )


# 🔘 Кнопки
async def buttons(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    user_id = query.from_user.id

    # Проверка подписки при каждом действии
    if not await is_subscribed(user_id, context.bot):
        await query.answer("Подпишись на канал ❗", show_alert=True)
        return

    if query.data == "shop":
        keyboard = [
            [InlineKeyboardButton("📱 Телефон", callback_data="phone")],
            [InlineKeyboardButton("💻 Ноутбук", callback_data="laptop")],
            [InlineKeyboardButton("🔙 Назад", callback_data="back")]
        ]
        await query.edit_message_text("Выбери товар:", reply_markup=InlineKeyboardMarkup(keyboard))

    elif query.data == "phone":
        await query.edit_message_text("📱 Телефон — 500$\nНапиши /buy_phone")

    elif query.data == "laptop":
        await query.edit_message_text("💻 Ноутбук — 1000$\nНапиши /buy_laptop")

    elif query.data == "about":
        await query.edit_message_text("Мы крутой магазин 😎")

    elif query.data == "back":
        await start(query, context)


# 🔄 Проверка подписки кнопкой
async def check_sub(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    user_id = query.from_user.id

    if await is_subscribed(user_id, context.bot):
        await query.message.delete()
        await start(update, context)
    else:
        await query.answer("Ты ещё не подписан ❌", show_alert=True)


# 💰 Покупка
async def buy_phone(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Ты купил телефон 🎉")

async def buy_laptop(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Ты купил ноутбук 🎉")


# ▶️ Запуск
app = ApplicationBuilder().token(TOKEN).build()

app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("buy_phone", buy_phone))
app.add_handler(CommandHandler("buy_laptop", buy_laptop))
app.add_handler(CallbackQueryHandler(buttons))
app.add_handler(CallbackQueryHandler(check_sub, pattern="check_sub"))

app.run_polling()
