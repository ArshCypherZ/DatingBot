import logging
from typing import Union

from aiogram import types
from aiogram.dispatcher.handler import CancelHandler
from aiogram.dispatcher.middlewares import BaseMiddleware

from bot.database.methods.select import get_user_data


class IsUserExist(BaseMiddleware):
    def __init__(self):
        super(IsUserExist, self).__init__()

    async def on_process_message(self, message: types.Message, data: dict):
        user = await get_user_data(message.from_user.id)
        command = ""

        logging.info(data)

        try:
            command = data["command"].command
        except Exception:
            pass

        if user is None and command != "start":
            await message.answer("You are not registered! To register, write /start")
            raise CancelHandler()
        elif user is None:
            return
        else:
            await self.check_user_ban(message)

    async def on_process_callback_query(self, call: types.CallbackQuery, data: dict):
        user = await get_user_data(call.from_user.id)

        logging.info(data)

        if user is None:
            try:
                await call.message.answer(
                    "You are not registered! To register, write /start"
                )
            except Exception:
                pass
            raise CancelHandler()
        else:
            await self.check_user_ban(call)

    async def check_user_ban(
        self,
        message: Union[None, types.Message] = None,
        call: Union[None, types.CallbackQuery] = None,
    ):
        user = await get_user_data(message.from_user.id)
        if call:
            if user["is_banned"]:
                await call.message.answer("You have been blocked!")
                raise CancelHandler()
        elif message:
            if user["is_banned"]:
                await message.answer("You have been blocked!")
                raise CancelHandler()
