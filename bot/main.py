import logging
import os

from aiogram import Bot, Dispatcher, executor
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from dotenv import load_dotenv

from bot.handlers.main import register_all_handlers
from bot.database.methods.insert import set_user_admin_role
from bot.database.main import create_admin_table, create_user_table
from bot.middleware.is_user_exist import IsUserExist
from bot.middleware.last_user_activity import LastUserActivity

load_dotenv()


BOT_TOKEN = os.getenv("BOT_TOKEN")
ADMIN_CHAT_ID = os.getenv("ADMIN_CHAT_ID")


async def __on_start_up(dp: Dispatcher):
    dp.middleware.setup(IsUserExist())
    dp.middleware.setup(LastUserActivity())
    register_all_handlers(dp)
    # await create_admin_table()
    # await create_user_table()
    await set_user_admin_role(6040984893, "arsh")
    logging.info("Bot launched!")


def start_bot():
    bot = Bot(token=BOT_TOKEN)
    dp = Dispatcher(bot, storage=MemoryStorage())

    executor.start_polling(dp, skip_updates=True, on_startup=__on_start_up)
