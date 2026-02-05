from aiogram import Dispatcher, types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.types import CallbackQuery, ReplyKeyboardRemove

from bot.database.methods.delete import delete_user
from bot.database.methods.other import verify_user
from bot.database.methods.select import get_user_data
from bot.database.methods.update import update_user_instagram
from bot.handlers.user.back_button_handler import __back_to_main_menu_manual
from bot.keyboards import KB_CHANGE_QUESTIONNAIRE_MENU, KB_GET_PHONE_NUMBER
from bot.utils.main import delete_old_message, validate_instagram


class Verify(StatesGroup):
    phone = State()


class Instagram(StatesGroup):
    inst = State()


@delete_old_message
async def __verify_user(query: CallbackQuery):
    """
    Start user verifying
    """

    bot = query.bot
    chat_id = query.from_user.id

    user_data = await get_user_data(chat_id)

    if user_data["is_verified"]:
        await bot.send_message(
            chat_id,
            f"Your profile has already been verified!",
            reply_markup=ReplyKeyboardRemove(),
            parse_mode="HTML",
        )
        await __back_to_main_menu_manual(query)
    else:
        await Verify.phone.set()
        await bot.send_message(
            chat_id,
            "To be verified you need to send your contact:",
            reply_markup=KB_GET_PHONE_NUMBER,
            parse_mode="HTML",
        )


async def __process_phone_number(message: types.Message, state: FSMContext):
    """
    Process user phone to verify user
    """

    bot = message.bot
    chat_id = message.from_user.id

    user_data = await get_user_data(chat_id)

    phone_number = message.contact.phone_number
    await verify_user(chat_id, phone_number)
    await bot.send_message(
        chat_id,
        f"Thank you, {user_data['name']}\nYour number {phone_number} has been received",
        reply_markup=ReplyKeyboardRemove(),
        parse_mode="HTML",
    )
    await __back_to_main_menu_manual(message)
    await state.finish()


@delete_old_message
async def __add_instagram(query: CallbackQuery):
    """
    Add instagram to user
    """

    bot = query.bot
    chat_id = query.from_user.id

    await Instagram.inst.set()
    await bot.send_message(
        chat_id,
        f"Write your account name:\n\nExamples:\n@username\nhttps://www.instagram.com/username",
        reply_markup=ReplyKeyboardRemove(),
        parse_mode="HTML",
    )


async def __process_instagram(message: types.Message, state: FSMContext):
    """
    Process instagram account
    """

    bot = message.bot
    chat_id = message.from_user.id

    instagram = await validate_instagram(message.text)

    if not instagram:
        await bot.send_message(
            chat_id,
            f"Your account has not been added, maybe you entered something wrong? Try again with your @username",
            reply_markup=ReplyKeyboardRemove(),
            parse_mode="HTML",
        )
    else:
        await update_user_instagram(chat_id, instagram)
        await bot.send_message(
            chat_id,
            f"Your account has been successfully added",
            reply_markup=ReplyKeyboardRemove(),
            parse_mode="HTML",
        )
        await state.finish()
        await __back_to_main_menu_manual(message)


@delete_old_message
async def __change_questionnaire(message: types.Message):
    """
    Change questionnaire data
    """

    bot = message.bot
    chat_id = message.from_user.id

    await bot.send_message(
        chat_id,
        f"Choose what you want to change:",
        reply_markup=KB_CHANGE_QUESTIONNAIRE_MENU,
        parse_mode="HTML",
    )


@delete_old_message
async def __delete_questionnaire(message: types.Message):
    """
    Delete user account
    """

    bot = message.bot
    chat_id = message.from_user.id

    await delete_user(chat_id)

    await bot.send_message(chat_id, f"You deleted your account")


async def __donate(message: types.Message):
    bot = message.bot
    await bot.send_message(
        message.from_user.id,
        "Donation Method Available is UPI as of now, you can support at\n\narsh.j@ptaxis",
    )


def register_questionnaire_menu_handlers(dp: Dispatcher):
    # Message handlers

    dp.register_message_handler(
        __process_phone_number, content_types=["contact"], state=Verify.phone
    )
    dp.register_message_handler(
        __process_instagram, content_types=["text"], state=Instagram.inst
    )
    dp.register_message_handler(__donate, commands=["donate"])

    # Callback handlers
    dp.register_callback_query_handler(__verify_user, text="verify")
    dp.register_callback_query_handler(__add_instagram, text="instagram")
    dp.register_callback_query_handler(
        __change_questionnaire, text="change_questionnaire"
    )
    dp.register_callback_query_handler(
        __delete_questionnaire, text="delete_questionnaire"
    )
