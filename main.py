import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.filters import CommandStart
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import FSMContext
from aiogram.fsm.storage.memory import MemoryStorage

TOKEN = "8754551838:AAE-8Du0lEB0e_rhou0F7Mo7dUZNcRgLsMw"
CHANNEL_ID = "@tg263e"  # или -100xxxxxxxx

bot = Bot(token=TOKEN)
dp = Dispatcher(storage=MemoryStorage())

# -------- СОСТОЯНИЯ --------
class MenuState(StatesGroup):
    main = State()
    products = State()
    settings = State()
    change_name = State()

# -------- ПРОВЕРКА ПОДПИСКИ --------
async def check_sub(user_id):
    member = await bot.get_chat_member(CHANNEL_ID, user_id)
    return member.status in ["member", "administrator", "creator"]

# -------- КНОПКА ПОДПИСКИ --------
def sub_kb():
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="📢 Подписаться", url=f"https://t.me/{CHANNEL_ID[1:]}")],
        [InlineKeyboardButton(text="✅ Проверить", callback_data="check_sub")]
    ])

# -------- МЕНЮ --------
def main_menu():
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="📦 Каталог", callback_data="catalog")],
        [InlineKeyboardButton(text="⚙️ Настройки", callback_data="settings")]
    ])

# -------- СТАРТ --------
@dp.message(CommandStart())
async def start(message: types.Message, state: FSMContext):

    if not await check_sub(message.from_user.id):
        await message.answer(
            "❌ Подпишись на канал, чтобы пользоваться ботом",
            reply_markup=sub_kb()
        )
        return

    await state.set_state(MenuState.main)
    await message.answer("🏠 Главное меню:", reply_markup=main_menu())

# -------- ПРОВЕРКА КНОПКИ --------
@dp.callback_query(lambda c: c.data == "check_sub")
async def recheck(call: types.CallbackQuery, state: FSMContext):

    if await check_sub(call.from_user.id):
        await state.set_state(MenuState.main)
        await call.message.edit_text("✅ Доступ открыт!", reply_markup=main_menu())
    else:
        await call.answer("Ты ещё не подписался ❌", show_alert=True)

# -------- ЗАЩИТА ВСЕХ ДЕЙСТВИЙ --------
@dp.callback_query()
async def callbacks(call: types.CallbackQuery, state: FSMContext):

    if not await check_sub(call.from_user.id):
        await call.message.answer("❌ Сначала подпишись", reply_markup=sub_kb())
        return

    if call.data == "catalog":
        await call.message.edit_text("📦 Каталог (пример)")
