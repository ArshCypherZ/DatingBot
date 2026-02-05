from aiogram import Dispatcher, types
from aiogram.dispatcher.filters import Text
from aiogram.types import CallbackQuery, InputFile

from bot.keyboards import get_help_keyboard
from bot.utils.main import decode_callback_data, delete_old_message


@delete_old_message
async def __help(message: types.Message):
    """
    Show help
    """

    bot = message.bot
    chat_id = message.from_user.id

    await bot.send_photo(
        chat_id,
        photo=InputFile("bot/img/Frame1.jpg"),
        reply_markup=await get_help_keyboard(0),
        parse_mode="HTML",
    )


@delete_old_message
async def __help_page(query: CallbackQuery):
    """
    Show help
    """

    bot = query.bot
    chat_id = query.from_user.id

    page = int(await decode_callback_data(query))

    await bot.send_photo(
        chat_id,
        photo=InputFile(f"bot/img/Frame{page+1}.jpg"),
        reply_markup=await get_help_keyboard(page),
        parse_mode="HTML",
    )


def register_help_handlers(dp: Dispatcher):
    # Message handlers

    dp.register_message_handler(__help, commands=["help"])

    # Callback handlers
    dp.register_callback_query_handler(__help_page, Text(startswith="page_"))
