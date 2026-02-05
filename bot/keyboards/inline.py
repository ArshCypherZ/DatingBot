from typing import Final

from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

KB_CONTINUE_REGISTRATION: Final = InlineKeyboardMarkup(1)
KB_CONTINUE_REGISTRATION.add(
    InlineKeyboardButton("Continue", callback_data="continue_regestration")
)

KB_GENDER_SELECTION: Final = InlineKeyboardMarkup(2)
KB_GENDER_SELECTION.add(
    InlineKeyboardButton("🙎‍♂️ Male", callback_data="gender_male"),
    InlineKeyboardButton("🙎‍♀️ Female", callback_data="gender_female"),
)

KB_GENDER_IDENTITY: Final = InlineKeyboardMarkup(2)
KB_GENDER_IDENTITY.add(
    InlineKeyboardButton("I am a Boy 🙎‍♂️", callback_data="gender_male"),
    InlineKeyboardButton("I am a Girl 🙎‍♀️", callback_data="gender_female"),
)

KB_CHOOSE_YES_OR_NOT: Final = InlineKeyboardMarkup(2)
KB_CHOOSE_YES_OR_NOT.add(
    InlineKeyboardButton("Yes", callback_data="yes"),
    InlineKeyboardButton("NO", callback_data="no"),
)

KB_MENU: Final = InlineKeyboardMarkup(2)
KB_MENU.add(
    InlineKeyboardButton("👤️ My questionnaire", callback_data="my_questionnaire"),
    InlineKeyboardButton("⚙️ Filters", callback_data="filters"),
    InlineKeyboardButton("💌 Find a pair", callback_data="find"),
    InlineKeyboardButton("🆘 Support", callback_data="support"),
)

KB_QUESTIONNAIRE_MENU: Final = InlineKeyboardMarkup(2)
KB_QUESTIONNAIRE_MENU.add(
    InlineKeyboardButton(" ✅ Verification", callback_data="verify"),
    InlineKeyboardButton(
        "⚙️ Change Questionnaire", callback_data="change_questionnaire"
    ),
    InlineKeyboardButton("📸 Instagram", callback_data="instagram"),
    InlineKeyboardButton(
        "🚫 Delete questionnaire", callback_data="delete_questionnaire"
    ),
    InlineKeyboardButton("🔙 Back", callback_data="back"),
)

KB_CHANGE_QUESTIONNAIRE_MENU: Final = InlineKeyboardMarkup(2)
KB_CHANGE_QUESTIONNAIRE_MENU.add(
    InlineKeyboardButton("Name", callback_data="change_name"),
    InlineKeyboardButton("Gender", callback_data="change_gender"),
    InlineKeyboardButton("Age", callback_data="change_age"),
    InlineKeyboardButton("City", callback_data="change_location"),
    InlineKeyboardButton("Photo", callback_data="change_photo"),
    InlineKeyboardButton("About", callback_data="change_description"),
    InlineKeyboardButton("🔙 Back", callback_data="back"),
)

KB_FILTERS_MENU: Final = InlineKeyboardMarkup(2)
KB_FILTERS_MENU.add(
    InlineKeyboardButton("🚻 Gender of partner", callback_data="target_gender"),
    InlineKeyboardButton("🔙 Back", callback_data="back"),
)

KB_QUESTIONNAIRE_REVIEW: Final = InlineKeyboardMarkup(2)
KB_QUESTIONNAIRE_REVIEW.add(
    InlineKeyboardButton("👍", callback_data="like"),
    InlineKeyboardButton("👎", callback_data="dislike"),
    InlineKeyboardButton("🔙 Back", callback_data="back"),
)

KB_SUPPORT_MENU_USER: Final = InlineKeyboardMarkup(1)
KB_SUPPORT_MENU_USER.add(
    InlineKeyboardButton("Write to operator", callback_data="start_support_chat"),
    InlineKeyboardButton("End Session", callback_data="end_support_chat"),
)

KB_SUPPORT_MENU_USER_END: Final = InlineKeyboardMarkup(1)
KB_SUPPORT_MENU_USER_END.add(
    InlineKeyboardButton("End Session", callback_data="end_support_chat"),
)
