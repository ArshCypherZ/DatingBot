from aiogram import Dispatcher, types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.types import CallbackQuery, ReplyKeyboardRemove

from bot.database.methods.update import (
    update_target_gender,
)
from bot.handlers.user.back_button_handler import __back_to_main_menu_manual
from bot.keyboards import KB_CHOOSE_YES_OR_NOT, KB_GENDER_SELECTION, KB_GET_LOCATION
from bot.utils.main import (
    decode_callback_data,
    delete_old_message,
    get_location_by_coordinates,
    get_location_by_name,
)


class FilterCity(StatesGroup):
    location = State()


class FilterGender(StatesGroup):
    gender = State()


class FilterAge(StatesGroup):
    age_min = State()
    age_max = State()



async def __process_target_location_change(message: types.Message, state: FSMContext):
    """
    Process user location
    """

    bot = message.bot
    chat_id = message.from_user.id

    user_location = await get_location_by_coordinates(
        message.location.latitude, message.location.longitude
    )

    await state.update_data(location=user_location)

    await bot.send_message(
        chat_id, f"{user_location} is your city?", reply_markup=KB_CHOOSE_YES_OR_NOT
    )


async def __location_target_change_incorrect(query: CallbackQuery):
    """
    Called if location incorrect
    """

    bot = query.bot
    chat_id = query.from_user.id

    await bot.send_message(chat_id, f"Try to send the name of the settlement")
    await query.answer()


async def __find_location_target_by_name_change(
    message: types.Message, state: FSMContext
):
    """
    Called to find location by name
    """

    bot = message.bot
    chat_id = message.from_user.id

    user_location = await get_location_by_name(message.text)

    await state.update_data(location=user_location)

    if user_location == "not found":
        await bot.send_message(
            chat_id, "Your settlement was not found, please try again"
        )
    else:
        await bot.send_message(
            chat_id, f"{user_location} is your city?", reply_markup=KB_CHOOSE_YES_OR_NOT
        )


@delete_old_message
async def __filter_change_age(query: CallbackQuery):
    """
    Change user target age
    """

    bot = query.bot
    chat_id = query.from_user.id

    await FilterAge.age_min.set()
    await bot.send_message(chat_id, "Enter minimum age:", parse_mode="HTML")


async def __filter_process_age_change_invalid(message: types.Message):
    """
    If age is invalid
    """

    bot = message.bot
    chat_id = message.from_user.id

    await bot.send_message(chat_id, "Age must be a number!")


async def __filter_process_age_change_out_of_range(message: types.Message):
    """
    If age is out of range
    """

    bot = message.bot
    chat_id = message.from_user.id

    await bot.send_message(chat_id, "Age must be between 16 and 50!")





@delete_old_message
async def __change_target_gender_filter(query: CallbackQuery):
    """
    Change user target gender
    """

    bot = query.bot
    chat_id = query.from_user.id

    await FilterGender.gender.set()
    await bot.send_message(
        chat_id, "Select who you want to find:", reply_markup=KB_GENDER_SELECTION
    )


async def __process_targer_gender_filter(query: CallbackQuery, state: FSMContext):
    """
    Process user target gender
    """

    bot = query.bot
    chat_id = query.from_user.id

    await update_target_gender(chat_id, await decode_callback_data(query))

    await state.finish()
    await bot.send_message(chat_id, "Data saved")
    await query.answer()
    await __back_to_main_menu_manual(query)


def register_filter_menu_handlers(dp: Dispatcher):
    # Message handlers
    dp.register_message_handler(
        __process_target_location_change,
        content_types=["location"],
        state=FilterCity.location,
    )
    dp.register_message_handler(
        __find_location_target_by_name_change,
        content_types=["text"],
        state=FilterCity.location,
    )
    dp.register_message_handler(
        __filter_process_age_change_invalid,
        lambda message: not message.text.isdigit(),
        state=FilterAge,
    )
    dp.register_message_handler(
        __filter_process_age_change_out_of_range,
        lambda message: int(message.text) < 16 or int(message.text) > 50,
        state=FilterAge,
    )

    # Callback handlers
    dp.register_callback_query_handler(
        __change_target_gender_filter, text="target_gender"
    )
    dp.register_callback_query_handler(
        __process_targer_gender_filter,
        Text(startswith="gender_"),
        state=FilterGender.gender,
    )
