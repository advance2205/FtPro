import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.filters import CommandStart
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

TOKEN = "8754551838:AAE-8Du0lEB0e_rhou0F7Mo7dUZNcRgLsMw"

bot = Bot(token=TOKEN)
dp = Dispatcher()

# --- Главное меню ---
def main_menu():
    kb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="📦 Товары", callback_data="products")],
        [InlineKeyboardButton(text="⚙️ Настройки", callback_data="settings")]
    ])
    return kb

# --- Подменю товаров ---
def products_menu():
    kb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="📱 Телефоны", callback_data="phones")],
        [InlineKeyboardButton(text="💻 Ноутбуки", callback_data="laptops")],
        [InlineKeyboardButton(text="⬅️ Назад", callback_data="back_main")]
    ])
    return kb

# --- Подменю настроек ---
def settings_menu():
    kb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🔔 Уведомления", callback_data="notify")],
        [InlineKeyboardButton(text="🌐 Язык", callback_data="lang")],
        [InlineKeyboardButton(text="⬅️ Назад", callback_data="back_main")]
    ])
    return kb

# --- Старт ---
@dp.message(CommandStart())
async def start(message: types.Message):
    await message.answer("Главное меню:", reply_markup=main_menu())

# --- Обработка кнопок ---
@dp.callback_query()
async def menu_handler(call: types.CallbackQuery):

    # Главное меню
    if call.data == "back_main":
        await call.message.edit_text("Главное меню:", reply_markup=main_menu())

    # Товары
    elif call.data == "products":
        await call.message.edit_text("Выбери категорию:", reply_markup=products_menu())

    elif call.data == "phones":
        await call.message.edit_text("📱 Вот список телефонов")

    elif call.data == "laptops":
        await call.message.edit_text("💻 Вот список ноутбуков")

    # Настройки
    elif call.data == "settings":
        await call.message.edit_text("Настройки:", reply_markup=settings_menu())

    elif call.data == "notify":
        await call.message.edit_text("🔔 Настройки уведомлений")

    elif call.data == "lang":
        await call.message.edit_text("🌐 Выбор языка")

# --- Запуск ---
async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
