from aiogram import types
from aiogram.dispatcher.middlewares import BaseMiddleware

from bot.database.methods.update import update_user_last_active_time


class LastUserActivity(BaseMiddleware):
    def __init__(self):
        super(LastUserActivity, self).__init__()

    async def on_process_message(self, message: types.Message, data: dict):
        await update_user_last_active_time(message.from_user.id)

    async def on_process_callback_query(self, call: types.CallbackQuery, data: dict):
        await update_user_last_active_time(call.from_user.id)
