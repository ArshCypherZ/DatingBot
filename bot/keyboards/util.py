from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup


async def get_questionnaire_answear_keyboard(user_data):
    kb_questionnaire_answear = InlineKeyboardMarkup(2)
    kb_questionnaire_answear.add(
        InlineKeyboardButton("👍", callback_data=f"like_{user_data['telegram_id']}"),
        InlineKeyboardButton("👎", callback_data="dislike_answear"),
    )
    return kb_questionnaire_answear


async def get_help_keyboard(page):
    page_next = page + 1
    page_prev = page - 1
    if page - 1 < 0:
        page_prev = 2
    if page + 1 > 2:
        page_next = 0
    kb_help = InlineKeyboardMarkup(2)
    kb_help.add(
        InlineKeyboardButton("⬅️", callback_data=f"page_{page_prev}"),
        InlineKeyboardButton("➡️", callback_data=f"page_{page_next}"),
        InlineKeyboardButton("🔙 Back", callback_data="back"),
    )
    return kb_help
