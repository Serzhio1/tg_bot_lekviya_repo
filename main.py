import asyncio
from aiogram import Bot, Dispatcher
from os import getenv
from dotenv import load_dotenv
from handlers import greeting_handler, add_notepad_handler, add_lecture_handler, my_notepads_handler, my_lecture_handler, add_image_to_lecture_handler
from database.db import async_engine, Base


async def main():
    load_dotenv()
    bot = Bot(token=getenv("BOT_TOKEN"))
    dp = Dispatcher()

    async with async_engine.begin() as conn:
        # await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)

    dp.include_router(greeting_handler.router)
    dp.include_router(add_notepad_handler.router)
    dp.include_router(add_lecture_handler.router)
    dp.include_router(my_notepads_handler.router)
    dp.include_router(my_lecture_handler.router)
    dp.include_router(add_image_to_lecture_handler.router)

    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
