from aiogram import Dispatcher, types

from bot.database.methods.select import (
    get_active_users_count_by_data,
    get_fake_users_count,
    get_new_users_count_by_data,
    get_user_count,
    is_user_admin,
)


async def __stats(message: types.Message):
    """
    Show bot statistics
    """

    bot = message.bot
    chat_id = message.from_user.id

    if await is_user_admin(chat_id):
        total_users = await get_user_count()

        await bot.send_message(
            chat_id,
            f"Total users: {total_users}",
        )


def register_admin_statisctic_handlers(dp: Dispatcher):
    # Message handlers

    dp.register_message_handler(__stats, commands=["stats"])
