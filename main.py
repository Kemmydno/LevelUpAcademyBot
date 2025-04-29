import asyncio
import logging
import os
from aiogram import Bot, Dispatcher, types
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiohttp import web

# Токен бота
TOKEN = '7470615660:AAFe853HvoM_y7sPi9mAt4j7e_N_jDfbqSo'  # <-- Вставил твой токен!

# Настройка логов
logging.basicConfig(level=logging.INFO)

# Инициализация бота и диспетчера
bot = Bot(token=TOKEN)
dp = Dispatcher(bot)

# Клавиатура
keyboard = InlineKeyboardMarkup(row_width=1)
keyboard.add(
    InlineKeyboardButton(text="📚 Перейти в каталог курсов", url="https://t.me/LevelUpAcademy4you"),
    InlineKeyboardButton(text="📚 Купить отдельный курс", callback_data="buy_course"),
    InlineKeyboardButton(text="🎁 Купить все курсы", callback_data="buy_all")
)

# Обработчик команды /start
@dp.message_handler(commands=['start'])
async def send_welcome(message: types.Message):
    await message.answer(
        "👋 Добро пожаловать в LevelUp Academy!\n🚀 Здесь вы найдёте лучшие курсы для развития своих навыков.\n\nВыберите действие ниже:",
        reply_markup=keyboard
    )

# Обработчик кнопок
@dp.callback_query_handler(lambda c: c.data)
async def process_callback(callback_query: types.CallbackQuery):
    if callback_query.data == "buy_course":
        await bot.answer_callback_query(callback_query.id)
        await bot.send_message(callback_query.from_user.id, "Для покупки курса напишите в поддержку: @CanUFixMePls")
    elif callback_query.data == "buy_all":
        await bot.answer_callback_query(callback_query.id)
        await bot.send_message(callback_query.from_user.id, "Для покупки полного пакета всех курсов напишите в поддержку: @CanUFixMePls")

# Фиктивный веб-сервер для Railway
async def handle(request):
    return web.Response(text="Bot is running.")

async def run_web_app():
    app = web.Application()
    app.router.add_get("/", handle)
    runner = web.AppRunner(app)
    await runner.setup()
    site = web.TCPSite(runner, "0.0.0.0", int(os.environ.get("PORT", 10000)))
    await site.start()

# Основной запуск
async def main():
    await asyncio.gather(
        run_web_app(),
        dp.start_polling()
    )

if __name__ == "__main__":
    asyncio.run(main())
