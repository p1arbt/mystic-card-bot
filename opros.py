import asyncio
import logging
from aiogram import Bot, Dispatcher, types
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.filters import Command
from aiogram.enums import ChatMemberStatus

# 🔴 Твой токен и канал
BOT_TOKEN = "8172354164:AAFEeTSHw577ok5gGxC2v-Sq54bsilM3vNE"
CHANNEL_ID = "@taina_goroskop"

# Создаём бота и диспетчер
bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

# Логирование
logging.basicConfig(level=logging.INFO)

# Предсказания для карт
predictions = {
    "card_1": """🔮 Твоя карта - *Тень прошлого*
Твоя судьба хранит в себе древние уроки, которые не были усвоены. 
Возможно, сейчас настал момент, чтобы отпустить тяжесть старых обид или нерешённых вопросов. 
Эта карта открывает дверь для прощения и внутренней гармонии. 
Прими вызов и освободи свою душу.""",

    "card_2": """🔮 Твоя карта - *Звезда путеводная*
Ты стоишь на пороге важного выбора, и звёзды направляют твоё сердце. 
Эта карта говорит о том, что ты уже на верном пути, и впереди тебя ждёт светлый момент. 
Однако, будь готов к важному решению, которое станет переломным. 
Ты не один — твой ангел-хранитель рядом.""",

    "card_3": """🔮 Твоя карта - *Врата изменений*
Энергия перемен на пороге твоей жизни. 
Возможно, ты чувствуешь, что что-то должно измениться, но не знаешь, с чего начать. 
Эта карта подскажет, что новые начинания могут быть не так страшны, как кажутся. 
Перемены принесут тебе не только испытания, но и несметные возможности для роста. 
Прими их с открытым сердцем."""
}

# Словарь для хранения выбора пользователей
user_choices = {}

# Клавиатура
keyboard = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="🔮 Карта №1", callback_data="card_1")],
    [InlineKeyboardButton(text="🔮 Карта №2", callback_data="card_2")],
    [InlineKeyboardButton(text="🔮 Карта №3", callback_data="card_3")]
])

# Функция обработки выбора карт
@dp.callback_query(lambda c: c.data.startswith("card_"))
async def process_callback(callback_query: types.CallbackQuery):
    user_id = callback_query.from_user.id
    
    if user_id in user_choices:
        await bot.send_message(user_id, "Вы уже выбрали карту! Изменить выбор нельзя.")
        await callback_query.answer()
        return
    
    user_choices[user_id] = callback_query.data
    prediction = predictions.get(callback_query.data, "Ошибка.")
    await bot.send_message(user_id, f"✨ Ваше предсказание: {prediction}")
    await callback_query.answer()

# Команда /send_poll для отправки опроса в канал
@dp.message(Command("send_poll"))
async def send_poll(message: types.Message):
    if message.chat.id == message.from_user.id:
        post_text = """🌙 *Загадка судьбы...*
        \nВыбери свою карту и узнай предсказание!"""
        await bot.send_message(CHANNEL_ID, post_text, reply_markup=keyboard, parse_mode="Markdown")
        await message.answer("✅ Опрос отправлен в канал!")

# Запуск бота
async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
