import asyncio
from aiogram import Bot, Dispatcher

from tg_token import tg_token
from user_handlers import user_router

async def main():
    bot = Bot(token=tg_token)
    dp = Dispatcher()
    dp.include_router(user_router)
    await dp.start_polling(bot)


if __name__ == '__main__':
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("bot shut down")