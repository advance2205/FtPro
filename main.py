
import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
import openai

BOT_TOKEN = "8754551838:AAE-8Du0lEB0e_rhou0F7Mo7dUZNcRgLsMw"
OPENAI_API_KEY = "YOUR_OPENAI_KEY"

openai.api_key = OPENAI_API_KEY

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

def get_keyboard(topic):
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🔄 Перегенерировать", callback_data=f"regen:{topic}")],
        [InlineKeyboardButton(text="➕ Ещё карточка", callback_data=f"more:{topic}")]
    ])

async def generate_prompt(topic: str):
    prompt = f'''
Создай идею визуальной обучающей карточки по теме: {topic}.
Верни:
Заголовок:
Описание изображения:
Короткий текст:
'''

    response = openai.ChatCompletion.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}]
    )

    return response['choices'][0]['message']['content']

async def generate_image(prompt_text: str):
    response = openai.Image.create(
        prompt=prompt_text,
        n=1,
        size="1024x1024"
    )
    return response['data'][0]['url']

async def send_card(chat_id, topic):
    await bot.send_message(chat_id, "🎨 Создаю карточку...")

    prompt = await generate_prompt(topic)
    image_url = await generate_image(prompt)

    await bot.send_photo(
        chat_id,
        photo=image_url,
        caption=f"Тема: {topic}",
        reply_markup=get_keyboard(topic)
    )

@dp.message()
async def handle_message(message: types.Message):
    topic = message.text
    await send_card(message.chat.id, topic)

@dp.callback_query()
async def handle_callback(callback: types.CallbackQuery):
    action, topic = callback.data.split(":")

    if action in ["regen", "more"]:
        await send_card(callback.message.chat.id, topic)

    await callback.answer()

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
