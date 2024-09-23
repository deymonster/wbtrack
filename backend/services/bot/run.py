import asyncio
import logging
import sys
import contextvars
from services.bot.bot_init import bot
from aiogram import Dispatcher
from services.bot.handlers import router

dp = Dispatcher()
dp.include_routers(router)


async def start_bot():
    print("Starting bot...")
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


async def stop_bot():
    print("Stopping bot...")
    await dp.stop_polling()
    await bot.session.close()
    print("Bot stopped!")


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    try:
        asyncio.run(start_bot())
    except KeyboardInterrupt:
        print('GoodBye!')



