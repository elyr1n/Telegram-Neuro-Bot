import os
import asyncio
import logging

from dotenv import load_dotenv
from aiogram import Bot, Dispatcher

from app.handlers import router as handlers
from app.database import init_db

init_db()


async def main():
    load_dotenv()

    bot = Bot(token=os.getenv("TOKEN"))
    dp = Dispatcher()
    dp.include_router(handlers)

    logging.basicConfig(level=logging.INFO)

    print("Бот запущен и готов к работе!")
    try:
        await dp.start_polling(bot)
    except (KeyboardInterrupt, SystemExit):
        print("Выключение бота...")
    finally:
        await bot.session.close()


if __name__ == "__main__":
    asyncio.run(main())
