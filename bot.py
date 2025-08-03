import logging
import os
from aiogram import Bot, Dispatcher, types
from aiogram.types import Message, InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils import executor
from aiogram.dispatcher.filters import Command
from aiogram.dispatcher.middlewares import BaseMiddleware
from aiogram.contrib.fsm_storage.memory import MemoryStorage

API_TOKEN = os.getenv("BOT_TOKEN")
ADMIN_ID = int(os.getenv("ADMIN_ID", "5026972781"))  # ID жены

logging.basicConfig(level=logging.INFO)
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot, storage=MemoryStorage())

user_payments = {}  # Примитивная БД

@dp.message_handler(commands=["start"])
async def cmd_start(message: Message):
    await message.answer("Привет! Чтобы получить доступ, отправь чек об оплате.")

@dp.message_handler(content_types=["photo", "document"])
async def handle_payment_proof(message: Message):
    user_id = message.from_user.id
    user_payments[user_id] = False  # пока не подтверждено
    forward_text = f"Пользователь @{message.from_user.username or user_id} прислал подтверждение оплаты. Подтвердить?"
    keyboard = InlineKeyboardMarkup().add(
        InlineKeyboardButton("✅ Подтвердить", callback_data=f"approve_{user_id}")
    )
    await bot.send_message(ADMIN_ID, forward_text, reply_markup=keyboard)
    await bot.forward_message(ADMIN_ID, message.chat.id, message.message_id)
    await message.answer("Спасибо! Ожидайте подтверждения.")

@dp.callback_query_handler(lambda c: c.data.startswith("approve_"))
async def approve_payment(callback_query: types.CallbackQuery):
    user_id = int(callback_query.data.split("_")[1])
    user_payments[user_id] = True
    await bot.send_message(user_id, "Оплата подтверждена! Вот ваш контент:")
    await bot.send_message(user_id, "🔓 Доступ открыт. Контент скоро появится.")
    await callback_query.answer("Подтверждено.")

if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)