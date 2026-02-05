import time

from aiogram import Dispatcher, types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.types import CallbackQuery, ReplyKeyboardRemove

from bot.database.methods.insert import create_fake_user
from bot.database.methods.other import register_user
from bot.database.methods.select import get_user_data, is_user_admin
from bot.database.methods.update import (
    update_account_active_status,
    update_target_gender,
    update_user_age,
    update_user_coordinates,
    update_user_description,
    update_user_gender,
    update_user_location,
    update_user_name,
    update_user_photo,
)
from bot.keyboards import (
    KB_CHOOSE_YES_OR_NOT,
    KB_CONTINUE_REGISTRATION,
    KB_CONTINUE_REGISTRATION,
    KB_GENDER_IDENTITY,
    KB_GENDER_SELECTION,
    KB_GET_LOCATION,

    KB_MENU,
)
from bot.utils.main import (
    decode_callback_data,
    get_location_by_coordinates,
    get_location_by_name,
    get_questionnaire,
)


class Form(StatesGroup):
    chat_id = State()  # Will be represented in storage as 'Form:chat_id'
    name = State()  # Will be represented in storage as 'Form:name'
    gender = State()  # Will be represented in storage as 'Form:gender'
    age = State()  # Will be represented in storage as 'Form:age'
    target_gender = State()  # Will be represented in storage as 'Form:target'
    location = State()  # Will be represented in storage as 'Form:location'
    description = State()  # Will be represented in storage as 'Form:description'
    photo = State()  # Will be represented in storage as 'Form:description'


async def __fake_registration(message: types.Message):
    """
    Conversation's entry point
    """

    bot = message.bot
    chat_id = message.from_user.id

    if await is_user_admin(chat_id):
        await Form.chat_id.set()
        state = Dispatcher.get_current().current_state()
        await state.update_data(chat_id=(int(time.time())))
        await create_fake_user((await state.get_data())["chat_id"])
        await Form.next()
        await bot.send_message(
            chat_id,
            "Fake questionnaire registration has started",
            reply_markup=KB_CONTINUE_REGISTRATION,
        )


async def __start(message: types.Message):
    """
    Conversation's entry point
    """

    bot = message.bot
    chat_id = message.from_user.id

    await Form.chat_id.set()
    state = Dispatcher.get_current().current_state()
    await state.update_data(chat_id=chat_id)
    await Form.next()

    if not await register_user(chat_id, message.from_user.username):
        await bot.send_message(
            chat_id,
            "Hello, I will help you find the perfect couple, for this, fill out your profile to start dating 👩❤️👨...",
            reply_markup=KB_CONTINUE_REGISTRATION,
        )
    else:
        try:
            user_data = await get_user_data(chat_id)
            await bot.send_photo(
                chat_id,
                caption=await get_questionnaire(user_data, 0),
                photo=str(user_data["photo_id"]),
                reply_markup=KB_MENU,
                parse_mode="HTML",
            )
            await state.finish()
        except BaseException:
            await bot.send_message(
                chat_id,
                "Hello, I will help you find the perfect couple, for this, fill out your profile to start dating 👩❤️👨...",
                reply_markup=KB_CONTINUE_REGISTRATION,
            )


async def __continue_registration(query: CallbackQuery):
    """
    Start of registration
    """

    bot = query.bot
    chat_id = query.from_user.id

    await bot.send_message(
        chat_id, "Write me your name, which everyone will see in the profile"
    )
    await query.answer()


async def __register_name(message: types.Message, state: FSMContext):
    """
    Process user name
    """

    bot = message.bot
    chat_id = message.from_user.id

    await update_user_name((await state.get_data())["chat_id"], message.text)

    await Form.next()
    await bot.send_message(chat_id, "Great, your name is recorded!")
    await bot.send_message(
        chat_id, "Are you a Boy or a Girl? (Select YOUR gender)", reply_markup=KB_GENDER_IDENTITY
    )


async def __register_name_invalid(message: types.Message):
    """
    Process user name
    """

    bot = message.bot
    chat_id = message.from_user.id

    await bot.send_message(chat_id, "Name must not be longer than 64 characters!")


async def __register_gender(query: CallbackQuery, state: FSMContext):
    """
    Process user gender
    """
    bot = query.bot
    chat_id = query.from_user.id

    await update_user_gender(
        (await state.get_data())["chat_id"], await decode_callback_data(query)
    )

    await Form.next()
    await bot.send_message(chat_id, "Your gender is entered!")
    await bot.send_message(chat_id, "Enter your age:")
    await query.answer()


async def __process_age_invalid(message: types.Message):
    """
    If age is invalid
    """

    bot = message.bot
    chat_id = message.from_user.id

    await bot.send_message(chat_id, "Age must be a number!\nEnter how old you are:")


async def __process_age_out_of_range(message: types.Message):
    """
    If age is out of range
    """

    bot = message.bot
    chat_id = message.from_user.id

    await bot.send_message(chat_id, "Age must be between 16 and 50!\nEnter your age:")


async def __process_age(message: types.Message, state: FSMContext):
    """
    Process user age
    """

    bot = message.bot
    chat_id = message.from_user.id

    await update_user_age((await state.get_data())["chat_id"], int(message.text))

    await Form.next()
    await bot.send_message(chat_id, "Great, age specified!")
    await bot.send_message(
        chat_id, "Now choose who you want to find? Please tell me which gender you want to see, do not choose your own gender by mistake.", reply_markup=KB_GENDER_SELECTION
    )


async def __process_target_gender(query: CallbackQuery, state: FSMContext):
    """
    Process user target gender
    """

    bot = query.bot
    chat_id = query.from_user.id

    await update_target_gender(
        (await state.get_data())["chat_id"], await decode_callback_data(query)
    )

    await Form.next()
    await bot.send_message(chat_id, "Great! Data saved!")
    await bot.send_message(
        chat_id,
        "Enter the city in which you live. To determine the exact location, you can click on the button below!:",
        reply_markup=KB_GET_LOCATION,
    )
    await query.answer()


async def __process_location(message: types.Message, state: FSMContext):
    """
    Process user location
    """

    bot = message.bot
    chat_id = message.from_user.id

    try:
        user_location = await get_location_by_coordinates(
            message.location.latitude, message.location.longitude
        )
        await update_user_coordinates(
            (await state.get_data())["chat_id"],
            message.location.latitude,
            message.location.longitude,
        )
        await state.update_data(location=user_location)

        await bot.send_message(
            chat_id, f"{user_location} is your city?", reply_markup=KB_CHOOSE_YES_OR_NOT
        )
    except ValueError:
        await bot.send_message(chat_id, "Please try again!")


async def __location_correct(query: CallbackQuery, state: FSMContext):
    """
    Called if location correct
    """

    bot = query.bot
    chat_id = query.from_user.id

    await update_user_location(
        (await state.get_data())["chat_id"], (await state.get_data())["location"]
    )

    await Form.next()
    await bot.send_message(
        chat_id,
        f"You have successfully added information about the settlement",
        reply_markup=ReplyKeyboardRemove(),
    )
    await bot.send_message(
        chat_id, f"Now write a little about yourself: (255 characters max)"
    )
    await query.answer()


async def __location_incorrect(query: CallbackQuery):
    """
    Called if location incorrect
    """

    bot = query.bot
    chat_id = query.from_user.id

    await bot.send_message(chat_id, f"Try to send the name of your settlement")
    await query.answer()


async def __find_location_by_name(message: types.Message, state: FSMContext):
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


async def __process_description_invalid(message: types.Message):
    """
    Called to process description
    """

    bot = message.bot
    chat_id = message.from_user.id

    await bot.send_message(
        chat_id, f"Your description must be less than 255 characters"
    )


async def __process_description(message: types.Message, state: FSMContext):
    """
    Called to process description
    """

    bot = message.bot
    chat_id = message.from_user.id

    await update_user_description((await state.get_data())["chat_id"], message.text)

    await Form.next()
    await bot.send_message(
        chat_id, f"You have successfully added information about yourself"
    )
    await bot.send_message(chat_id, f"Lastly, send me your photo (any will work):")


async def __process_photo(message: types.Message, state: FSMContext):
    """
    Called to process photo
    """

    bot = message.bot
    chat_id = message.from_user.id

    await update_user_photo(
        (await state.get_data())["chat_id"], str(message.photo[-1].file_id)
    )

    await bot.send_message(chat_id, f"Photo accepted!")

    await update_account_active_status((await state.get_data())["chat_id"], 1)

    await bot.send_message(
        chat_id,
        f"Yay!! 🎉 Registration successful! Enter /help if you need help with the bot. 😎",
    )

    user_data = await get_user_data((await state.get_data())["chat_id"])
    await bot.send_photo(
        chat_id,
        caption=await get_questionnaire(user_data, 0),
        photo=str(user_data["photo_id"]),
        reply_markup=KB_MENU,
        parse_mode="HTML",
    )
    await state.finish()


def register_regestration_handlers(dp: Dispatcher):
    # Message handlers

    dp.register_message_handler(__fake_registration, commands=["register_fake"])
    dp.register_message_handler(__start, commands=["start", "menu"])
    dp.register_message_handler(
        __register_name, content_types=["text"], state=Form.name
    )
    dp.register_message_handler(
        __register_name_invalid,
        lambda message: len(message.text) > 64,
        content_types=["text"],
        state=Form.name,
    )
    dp.register_message_handler(
        __process_age_invalid,
        lambda message: not message.text.isdigit(),
        state=Form.age,
    )
    dp.register_message_handler(
        __process_age_out_of_range,
        lambda message: int(message.text) < 16 or int(message.text) > 50,
        state=Form.age,
    )
    dp.register_message_handler(
        __process_age, lambda message: message.text.isdigit(), state=Form.age
    )
    dp.register_message_handler(
        __process_location, content_types=["location"], state=Form.location
    )
    dp.register_message_handler(
        __find_location_by_name, content_types=["text"], state=Form.location
    )
    dp.register_message_handler(
        __process_description_invalid,
        lambda message: len(message.text) > 255,
        state=Form.description,
    )
    dp.register_message_handler(
        __process_description, content_types=["text"], state=Form.description
    )
    dp.register_message_handler(
        __process_photo, content_types=["photo"], state=Form.photo
    )

    # Callback handlers

    dp.register_callback_query_handler(
        __continue_registration, text="continue_regestration", state=Form.name
    )
    dp.register_callback_query_handler(
        __register_gender, Text(startswith="gender_"), state=Form.gender
    )
    dp.register_callback_query_handler(
        __process_target_gender, Text(startswith="gender_"), state=Form.target_gender
    )
    dp.register_callback_query_handler(
        __location_correct, text="yes", state=Form.location
    )
    dp.register_callback_query_handler(
        __location_incorrect, text="no", state=Form.location
    )
