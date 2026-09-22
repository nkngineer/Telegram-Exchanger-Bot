from aiogram import Dispatcher, Bot
from dotenv import load_dotenv
from aiogram.client.session.aiohttp import AiohttpSession

from database.database import init_db
from handlers.main_handlers import main_router

import os
import asyncio


PROXY_URL = "socks5://127.0.0.1:10808" # Proxy URL for Xray

load_dotenv()
TG_API_TOKEN : str | None = os.getenv("TG_API_TOKEN")

session = AiohttpSession(proxy = PROXY_URL) # Proxy session for working with Xray

if TG_API_TOKEN:
    bot = Bot(token = TG_API_TOKEN, session = session)
else:
    raise ValueError("TG_API_TOKEN is not found")


dp = Dispatcher()
dp.include_router(main_router)





async def main():
    await init_db()
    await dp.start_polling(bot)




if __name__ == "__main__":
    asyncio.run(main())