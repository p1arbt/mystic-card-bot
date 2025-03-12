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
    "card_1": "✨ Вас ждёт неожиданный поворот судьбы...",
    "card_2": "🔮 Будьте внимательны к знакам Вселенной...",
    "card_3": "🌟 Скоро откроются новые возможности..."
}

# Словарь для хранения выбора пользователей
user_choices = {}

# Клавиатура с выбором карт
keyboard = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="🔮 Карта №1", callback_data="card_1")],
    [InlineKeyboardButton(text="🔮 Карта №2", callback_data="card_2")],
    [InlineKeyboardButton(text="🔮 Карта №3", callback_data="card_3")]
])

# Функция проверки подписки
async def check_subscription(user_id: int) -> bool:
    try:
        user_status = await bot.get_chat_member(CHANNEL_ID, user_id)
        return user_status.status in [ChatMemberStatus.MEMBER, ChatMemberStatus.ADMINISTRATOR, ChatMemberStatus.CREATOR]
    except:
        return False  # Ошибка при проверке подписки

# Обработка нажатий на кнопки
@dp.callback_query(lambda c: c.data.startswith("card_"))
async def process_callback(callback_query: types.CallbackQuery):
    user_id = callback_query.from_user.id

    # Проверяем подписку
    if not await check_subscription(user_id):
        await bot.send_message(user_id, "❌ Вы не подписаны на канал! Подпишитесь 👉 @taina_goroskop, чтобы получить предсказание.")
        await callback_query.answer()
        return

    # Проверяем, делал ли пользователь выбор ранее
    if user_id in user_choices:
        await bot.send_message(user_id, "⚠️ Вы уже выбрали карту! Изменить выбор нельзя.")
        await callback_query.answer()
        return

    # Сохраняем выбор пользователя
    user_choices[user_id] = callback_query.data

    # Отправляем предсказание
    prediction = predictions.get(callback_query.data, "Ошибка.")
    await bot.send_message(user_id, f"✨ Ваше предсказание: {prediction}")

    await callback_query.answer()

# Команда /start
@dp.message(Command("start"))
async def start(message: types.Message):
    await message.answer(
        "🔮 Выберите одну из карт судьбы, чтобы получить предсказание! После выбора изменить решение будет нельзя.\n\n👇 Выберите карту:",
        reply_markup=keyboard
    )

# Запуск бота
async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())