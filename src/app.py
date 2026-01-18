import asyncio
import logging

from aiogram import F
from aiogram.utils.callback_answer import CallbackAnswerMiddleware

from src.config import settings, COMMON_COMMANDS
from src.handlers import router as root_router
from src.loader import bot, dp
from src.agents.scheduler import scheduler


async def main():
    logging.basicConfig(level=logging.INFO)

    dp.callback_query.middleware(CallbackAnswerMiddleware(pre=True, cache_time=10))
    dp.include_router(root_router)

    await bot.set_my_commands(COMMON_COMMANDS)
    await bot.delete_webhook(drop_pending_updates=True)
    asyncio.create_task(scheduler())
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
