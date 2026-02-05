from aiogram import Dispatcher, types
from aiogram.utils.exceptions import BotBlocked

from bot.handlers.admin import (
    register_admin_statisctic_handlers,
    register_admin_support_handlers,
    register_admin_tools_handlers,
)
from bot.handlers.user import (
    register_back_button_handlers,
    register_change_questionnaire_menu_handlers,
    register_filter_menu_handlers,
    register_help_handlers,
    register_menu_handlers,
    register_questionnaire_handlers,
    register_questionnaire_menu_handlers,
    register_regestration_handlers,
    register_support_handlers,
)


async def catch_bot_blocked(update: types.Update, error):
    return True


def register_all_handlers(dp: Dispatcher):
    register_regestration_handlers(dp)
    register_menu_handlers(dp)
    register_back_button_handlers(dp)
    register_questionnaire_menu_handlers(dp)
    register_change_questionnaire_menu_handlers(dp)
    register_filter_menu_handlers(dp)
    register_questionnaire_handlers(dp)
    register_support_handlers(dp)
    register_help_handlers(dp)

    register_admin_support_handlers(dp)
    register_admin_statisctic_handlers(dp)
    register_admin_tools_handlers(dp)
    dp.register_errors_handler(catch_bot_blocked, exception=BotBlocked)
