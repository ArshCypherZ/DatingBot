from aiogram import Dispatcher
from aiogram.types import CallbackQuery

from bot.keyboards import KB_MENU
from bot.utils.main import delete_old_message


@delete_old_message
async def __back_to_main_menu(query: CallbackQuery):
    """
    Back to main menu
    """

    bot = query.bot
    chat_id = query.from_user.id

    await bot.send_message(
        chat_id,
        "You are returned to the main menu",
        reply_markup=KB_MENU,
        parse_mode="HTML",
    )


async def __back_to_main_menu_manual(query: CallbackQuery):
    """
    Back to main menu
    """

    bot = query.bot
    chat_id = query.from_user.id

    await bot.send_message(
        chat_id,
        "You are returned to the main menu",
        reply_markup=KB_MENU,
        parse_mode="HTML",
    )


def register_back_button_handlers(dp: Dispatcher):
    # Callback handlers
    dp.register_callback_query_handler(__back_to_main_menu, text="back")
