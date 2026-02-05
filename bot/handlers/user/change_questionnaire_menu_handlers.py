from aiogram import Dispatcher, types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.types import CallbackQuery, ReplyKeyboardRemove

from bot.database.methods.update import (
    update_user_age,
    update_user_coordinates,
    update_user_description,
    update_user_gender,
    update_user_location,
    update_user_name,
    update_user_photo,
)
from bot.handlers.user.back_button_handler import __back_to_main_menu_manual
from bot.keyboards import KB_CHOOSE_YES_OR_NOT, KB_GENDER_IDENTITY, KB_GENDER_SELECTION, KB_GET_LOCATION
from bot.utils.main import (
    decode_callback_data,
    delete_old_message,
    get_location_by_coordinates,
    get_location_by_name,
)



class ChangeName(StatesGroup):
    name = State()


class ChangeGender(StatesGroup):
    gender = State()


class ChangeAge(StatesGroup):
    age = State()


class ChangeLocation(StatesGroup):
    location = State()


class ChangePhoto(StatesGroup):
    photo = State()


class ChangeDescription(StatesGroup):
    description = State()


@delete_old_message
async def __change_name(query: CallbackQuery):
    """
    Change user name
    """

    bot = query.bot
    chat_id = query.from_user.id

    await ChangeName.name.set()
    await bot.send_message(
        chat_id,
        "Write me your name that everyone will see in the profile",
        reply_markup=ReplyKeyboardRemove(),
        parse_mode="HTML",
    )


async def __process_change_name(message: types.Message, state: FSMContext):
    """
    Process user name change
    """

    bot = message.bot
    chat_id = message.from_user.id

    await update_user_name(chat_id, message.text)

    await bot.send_message(chat_id, "Great, your name is recorded!")
    await __back_to_main_menu_manual(message)
    await state.finish()


async def __process_change_name_invalid(message: types.Message):
    """
    Process user name change too long
    """

    bot = message.bot
    chat_id = message.from_user.id

    await bot.send_message(chat_id, "Name must not be longer than 64 characters!")


@delete_old_message
async def __change_gender(query: CallbackQuery):
    """
    Change user gender
    """

    bot = query.bot
    chat_id = query.from_user.id

    await ChangeGender.gender.set()
    await bot.send_message(
        chat_id,
        "Are you a Boy or a Girl? (Select YOUR gender)",
        reply_markup=KB_GENDER_IDENTITY,
        parse_mode="HTML",
    )


async def __process_gender_change(query: CallbackQuery, state: FSMContext):
    """
    Process user gender
    """
    bot = query.bot
    chat_id = query.from_user.id

    await update_user_gender(chat_id, await decode_callback_data(query))

    await bot.send_message(chat_id, "Your gender is entered!")
    await __back_to_main_menu_manual(query)
    await state.finish()
    await query.answer()


@delete_old_message
async def __change_age(query: CallbackQuery):
    """
    Change user age
    """

    bot = query.bot
    chat_id = query.from_user.id

    await ChangeAge.age.set()
    await bot.send_message(chat_id, "Enter your age:", parse_mode="HTML")


async def __process_age_change_invalid(message: types.Message):
    """
    If age is invalid
    """

    bot = message.bot
    chat_id = message.from_user.id

    await bot.send_message(chat_id, "Age must be a number!\nEnter how old you are:")


async def __process_age_change_out_of_range(message: types.Message):
    """
    If age is out of range
    """

    bot = message.bot
    chat_id = message.from_user.id

    await bot.send_message(chat_id, "Age must be between 16 and 50!\nEnter your age:")


async def __process_age_change(message: types.Message, state: FSMContext):
    """
    Process user age
    """

    bot = message.bot
    chat_id = message.from_user.id

    await update_user_age(chat_id, int(message.text))

    await bot.send_message(chat_id, "Great, age specified!")
    await __back_to_main_menu_manual(message)
    await state.finish()


@delete_old_message
async def __change_location(query: CallbackQuery):
    """
    Change user location
    """

    bot = query.bot
    chat_id = query.from_user.id

    await ChangeLocation.location.set()
    await bot.send_message(
        chat_id,
        "Enter the city in which you live. To determine the exact location, you can click on the button below!:",
        reply_markup=KB_GET_LOCATION,
        parse_mode="HTML",
    )


async def __process_location_change(message: types.Message, state: FSMContext):
    """
    Process user location
    """

    bot = message.bot
    chat_id = message.from_user.id

    user_location = await get_location_by_coordinates(
        message.location.latitude, message.location.longitude
    )
    await update_user_coordinates(
        chat_id, message.location.latitude, message.location.longitude
    )

    await state.update_data(location=user_location)

    await bot.send_message(
        chat_id, f"{user_location} is your city?", reply_markup=KB_CHOOSE_YES_OR_NOT
    )


async def __location_change_correct(query: CallbackQuery, state: FSMContext):
    """
    Called if location correct
    """

    bot = query.bot
    chat_id = query.from_user.id

    await update_user_location(chat_id, (await state.get_data())["location"])

    await bot.send_message(
        chat_id,
        f"You have successfully added information about the settlement",
        reply_markup=ReplyKeyboardRemove(),
    )
    await state.finish()
    await query.answer()
    await __back_to_main_menu_manual(query)


async def __location_change_incorrect(query: CallbackQuery):
    """
    Called if location incorrect
    """

    bot = query.bot
    chat_id = query.from_user.id

    await bot.send_message(chat_id, f"Try to send the name of your settlement")
    await query.answer()


async def __find_location_by_name_change(message: types.Message, state: FSMContext):
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
async def __change_photo(query: CallbackQuery):
    """
    Change user photo
    """

    bot = query.bot
    chat_id = query.from_user.id

    await ChangePhoto.photo.set()
    await bot.send_message(
        chat_id,
        "Send me your photo:",
        reply_markup=ReplyKeyboardRemove(),
        parse_mode="HTML",
    )


async def __process_photo_change(message: types.Message, state: FSMContext):
    """
    Process user photo change
    """

    bot = message.bot
    chat_id = message.from_user.id

    await update_user_photo(chat_id, str(message.photo[-1].file_id))

    await bot.send_message(chat_id, "Photo accepted!")
    await __back_to_main_menu_manual(message)
    await state.finish()


@delete_old_message
async def __change_description(query: CallbackQuery):
    """
    Change user description
    """

    bot = query.bot
    chat_id = query.from_user.id

    await ChangeDescription.description.set()
    await bot.send_message(
        chat_id,
        "Write a little about yourself: (255 characters max)",
        reply_markup=ReplyKeyboardRemove(),
        parse_mode="HTML",
    )


async def __process_description_change_invalid(message: types.Message):
    """
    Process user description change invalid
    """

    bot = message.bot
    chat_id = message.from_user.id

    await bot.send_message(
        chat_id, f"Your description must be less than 255 characters"
    )


async def __process_change_description(message: types.Message, state: FSMContext):
    """
    Process user description change
    """

    bot = message.bot
    chat_id = message.from_user.id

    await update_user_description(chat_id, message.text)

    await bot.send_message(
        chat_id, "You have successfully added information about yourself"
    )
    await __back_to_main_menu_manual(message)
    await state.finish()


def register_change_questionnaire_menu_handlers(dp: Dispatcher):
    # Message handlers
    dp.register_message_handler(
        __process_change_name_invalid,
        lambda message: len(message.text) > 64,
        content_types=["text"],
        state=ChangeName.name,
    )
    dp.register_message_handler(
        __process_change_name,
        lambda message: len(message.text) < 64,
        content_types=["text"],
        state=ChangeName.name,
    )
    dp.register_message_handler(
        __process_age_change_invalid,
        lambda message: not message.text.isdigit(),
        state=ChangeAge.age,
    )
    dp.register_message_handler(
        __process_age_change_out_of_range,
        lambda message: int(message.text) < 16 or int(message.text) > 50,
        state=ChangeAge.age,
    )
    dp.register_message_handler(
        __process_age_change,
        lambda message: message.text.isdigit(),
        state=ChangeAge.age,
    )
    dp.register_message_handler(
        __process_location_change,
        content_types=["location"],
        state=ChangeLocation.location,
    )
    dp.register_message_handler(
        __find_location_by_name_change,
        content_types=["text"],
        state=ChangeLocation.location,
    )
    dp.register_message_handler(
        __process_photo_change, content_types=["photo"], state=ChangePhoto.photo
    )
    dp.register_message_handler(
        __process_description_change_invalid,
        lambda message: len(message.text) > 255,
        state=ChangeDescription.description,
    )
    dp.register_message_handler(
        __process_change_description,
        content_types=["text"],
        state=ChangeDescription.description,
    )

    # Callback handlers
    dp.register_callback_query_handler(__change_name, text="change_name")
    dp.register_callback_query_handler(__change_gender, text="change_gender")
    dp.register_callback_query_handler(
        __process_gender_change, Text(startswith="gender_"), state=ChangeGender.gender
    )
    dp.register_callback_query_handler(__change_age, text="change_age")
    dp.register_callback_query_handler(__change_location, text="change_location")
    dp.register_callback_query_handler(__change_photo, text="change_photo")
    dp.register_callback_query_handler(__change_description, text="change_description")
    dp.register_callback_query_handler(
        __location_change_correct, text="yes", state=ChangeLocation.location
    )
    dp.register_callback_query_handler(
        __location_change_incorrect, text="no", state=ChangeLocation.location
    )
