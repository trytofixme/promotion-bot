from aiogram import Bot, Dispatcher
from aiogram.client.session.aiohttp import AiohttpSession
from aiogram.client.telegram import TelegramAPIServer

from src.config import settings

if settings.bot.telegram_api_server:
    local_server = TelegramAPIServer.from_base(settings.bot.telegram_api_server)
    session = AiohttpSession(api=local_server)
    print(f"TEST MODE: Работаем через MOCK: {settings.bot.telegram_api_server}")
else:
    session = AiohttpSession()

bot = Bot(token=settings.bot.token.get_secret_value(), session=session)
dp = Dispatcher()
