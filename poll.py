from aiogram import Bot, Dispatcher, types
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils import executor

API_TOKEN = '8172354164:AAFEeTSHw577ok5gGxC2v-Sq54bsilM3vNE'  # Замените на токен вашего бота
CHANNEL_ID = '@taina_goroskop'  # Замените на ваш канал

bot = Bot(token=8172354164:AAFEeTSHw577ok5gGxC2v-Sq54bsilM3vNE)
dp = Dispatcher(bot)

@dp.message_handler(commands=['start'])
async def send_welcome(message: types.Message):
    # Создаём inline кнопки для выбора карты
    keyboard = InlineKeyboardMarkup(row_width=1)
    buttons = [
        InlineKeyboardButton("🔮 Карта №1", callback_data="card_1"),
        InlineKeyboardButton("🔮 Карта №2", callback_data="card_2"),
        InlineKeyboardButton("🔮 Карта №3", callback_data="card_3")
    ]
    keyboard.add(*buttons)

    # Текст поста с кнопками
    post_text = """
    *🌙 Загадка судьбы, скрытая за картами…*  
    
    Перед тобой три магические карты. Каждая скрывает важное послание.  
    Выбери свою карту и узнай предсказание!
    
    👇 Нажми на кнопку ниже, чтобы выбрать.
    """
    
    # Отправляем сообщение в канал с кнопками
    await bot.send_message(chat_id=CHANNEL_ID, text=post_text, reply_markup=keyboard, parse_mode="Markdown")

if __name__ == '__main__':
    executor.start_polling(dp)
