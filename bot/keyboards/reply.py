from typing import Final

from aiogram.types import KeyboardButton, ReplyKeyboardMarkup

KB_GET_LOCATION: Final = ReplyKeyboardMarkup(1, resize_keyboard=True)
KB_GET_LOCATION.add(
    KeyboardButton("Share Location", request_location=True),
)


KB_GET_PHONE_NUMBER: Final = ReplyKeyboardMarkup(1, resize_keyboard=True)
KB_GET_PHONE_NUMBER.add(
    KeyboardButton("Share number", request_contact=True),
)


KB_END_CHAT: Final = ReplyKeyboardMarkup(1, resize_keyboard=True)
KB_END_CHAT.add(
    KeyboardButton("End correspondence"),
)
