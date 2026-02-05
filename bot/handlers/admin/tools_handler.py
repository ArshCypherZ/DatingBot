from aiogram import Dispatcher, types

from bot.database.methods.insert import set_user_admin_role
from bot.database.methods.select import get_all_users, is_user_admin
from bot.database.methods.update import update_user_ban_state


async def __ban(message: types.Message):
    """
    Ban user by chat_id
    """

    bot = message.bot
    chat_id = message.from_user.id

    args = message.get_args().split()
    user_id = args[0] if args else ""

    if await is_user_admin(chat_id) and len(user_id) != 0:
        await update_user_ban_state(user_id, 1)
        await bot.send_message(chat_id, f"User is blocked")
        await bot.send_message(user_id, f"You have been banned. Contact @SpiralTechDivision to know more.")

async def __unban(message: types.Message):
    bot = message.bot
    chat_id = message.from_user.id
    args = message.get_args().split()
    user_id = args[0] if args else ""
    if await is_user_admin(chat_id) and len(user_id) != 0:
        await update_user_ban_state(user_id, 0)
        await bot.send_message(chat_id, f"User is unblocked")
        await bot.send_message(user_id, f"You have been unbanned. Contact @SpiralTechDivision to know more.")

async def __admin(message: types.Message):
    """
    Set user as admin by chat_id
    """

    bot = message.bot
    chat_id = message.from_user.id

    args = message.get_args().split()
    user_id = args[0] if args else ""

    if await is_user_admin(chat_id) and len(user_id) != 0:
        if await is_user_admin(user_id):
            await bot.send_message(chat_id, f"The user is already an administrator")
        else:
            await set_user_admin_role(user_id, 1)
            await bot.send_message(chat_id, f"User assigned by administrator")


async def __send_message_to_user(message: types.Message):
    """
    Send message to user by chat_id
    """

    bot = message.bot
    chat_id = message.from_user.id

    user_id = message.get_args().split(" ", 1)[0]

    message_text = message.get_args().split(" ", 1)[1]

    if await is_user_admin(chat_id) and len(user_id) != 0:
        try:
            await bot.send_message(user_id, message_text)
        except BaseException:
            await bot.send_message(chat_id, "Message not sent, something went wrong")


async def __send_message_to_all_users(message: types.Message):
    """
    Send message to all users
    """

    bot = message.bot
    chat_id = message.from_user.id

    message_text = message.get_args()

    if await is_user_admin(chat_id):
        for user in await get_all_users():
            try:
                await bot.send_message(user["telegram_id"], message_text)
            except BaseException:
                pass


def register_admin_tools_handlers(dp: Dispatcher):
    # Message handlers

    dp.register_message_handler(__ban, commands=["ban"])
    dp.register_message_handler(__admin, commands=["admin"])
    dp.register_message_handler(__send_message_to_user, commands=["send"])
    dp.register_message_handler(__send_message_to_all_users, commands=["send_all"])
    dp.register_message_handler(__unban, commands=["unban"])
