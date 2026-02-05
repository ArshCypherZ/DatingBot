from aiogram import Dispatcher
from aiogram.types import CallbackQuery

from bot.database.methods.select import get_user_data
from bot.keyboards import KB_FILTERS_MENU, KB_QUESTIONNAIRE_MENU, KB_SUPPORT_MENU_USER
from bot.utils.main import (
    add_age_filter_ending,
    delete_old_message,
    format_filters_data,
    get_questionnaire,
)
from bot.utils.questionnaire import get_other_questionnaire


@delete_old_message
async def __user_questionnaire(query: CallbackQuery):
    """
    Show user questionnaire and questionnaire menu
    """

    bot = query.bot
    chat_id = query.from_user.id

    user_data = await get_user_data(chat_id)

    await bot.send_photo(
        chat_id,
        caption=await get_questionnaire(user_data, 1),
        photo=str(user_data["photo_id"]),
        reply_markup=KB_QUESTIONNAIRE_MENU,
        parse_mode="HTML",
    )


@delete_old_message
async def __user_filters(query: CallbackQuery):
    """
    Show user questionnaire and questionnaire menu
    """

    bot = query.bot
    chat_id = query.from_user.id

    user_data = await format_filters_data(await get_user_data(chat_id))

    await bot.send_message(
        chat_id,
        f"Partner selection filter:\n\n🚻 Partner gender required: {user_data[0]}",
        reply_markup=KB_FILTERS_MENU,
        parse_mode="HTML",
    )


@delete_old_message
async def __find_target(query: CallbackQuery):
    """
    Show other questionnaires
    """

    await get_other_questionnaire(query)


@delete_old_message
async def __support(query: CallbackQuery):
    """
    Show support menu
    """

    bot = query.bot
    chat_id = query.from_user.id

    await bot.send_message(
        chat_id,
        f"Sorry but due to heavy amount of traffic, support option is removed, but you can ask for doubts/queries or report any bugs to this group chat- @SpiralTechDivision\n\n<b>Note:</b> Please don't spam, do not ask for gf/bf, and certainly no chit chat, this group is only for support.",
        parse_mode="HTML",
    )


def register_menu_handlers(dp: Dispatcher):
    # Callback handlers
    dp.register_callback_query_handler(__user_questionnaire, text="my_questionnaire")
    dp.register_callback_query_handler(__user_filters, text="filters")
    dp.register_callback_query_handler(__find_target, text="find")
    dp.register_callback_query_handler(__support, text="support")
