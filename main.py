import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.filters import CommandStart
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.fsm.storage.memory import MemoryStorage

TOKEN = "8754551838:AAE-8Du0lEB0e_rhou0F7Mo7dUZNcRgLsMw"
CHANNEL_ID = "@tg263e"

bot = Bot(token=TOKEN)
dp = Dispatcher(storage=MemoryStorage())

# -------- "БАЗА" --------
users_db = {}
# структура:
# user_id: {"subscribed": bool, "bonus": bool, "balance": int}

# -------- ПРОВЕРКА ПОДПИСКИ --------
async def check_sub(user_id):
    member = await bot.get_chat_member(CHANNEL_ID, user_id)
    return member.status in ["member", "administrator", "creator"]

# -------- КНОПКИ --------
def sub_kb():
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="📢 Подписаться", url=f"https://t.me/{CHANNEL_ID[1:]}")],
        [InlineKeyboardButton(text="✅ Проверить", callback_data="check_sub")]
    ])

def main_menu():
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="💰 Баланс", callback_data="balance")]
    ])

# -------- СТАРТ --------
@dp.message(CommandStart())
async def start(message: types.Message):
    user_id = message.from_user.id

    if user_id not in users_db:
        users_db[user_id] = {
            "subscribed": False,
            "bonus": False,
            "balance": 0
        }

    if not await check_sub(user_id):
        await message.answer("Подпишись, чтобы получить бонус 🎁", reply_markup=sub_kb())
        return

    await message.answer("Добро пожаловать!", reply_markup=main_menu())

# -------- ПРОВЕРКА --------
@dp.callback_query(lambda c: c.data == "check_sub")
async def check(call: types.CallbackQuery):
    user_id = call.from_user.id

    if await check_sub(user_id):
        user = users_db[user_id]

        # если бонус ещё не выдавался
        if not user["bonus"]:
            user["bonus"] = True
            user["balance"] += 100  # ← бонус

            await call.message.edit_text(
                "🎉 Ты получил 100 бонусов!\n\nТеперь можешь пользоваться ботом",
                reply_markup=main_menu()
            )
        else:
            await call.message.edit_text(
                "✅ Ты уже получал бонус",
                reply_markup=main_menu()
            )
    else:
        await call.answer("Сначала подпишись ❌", show_alert=True)

# -------- БАЛАНС --------
@dp.callback_query(lambda c: c.data == "balance")
async def balance(call: types.CallbackQuery):
    user = users_db[call.from_user.id]
    await call.answer(f"Баланс: {user['balance']} 💰", show_alert=True)

# -------- ЗАПУСК --------
async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
