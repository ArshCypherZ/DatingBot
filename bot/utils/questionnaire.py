import random
import logging

from bot.database.methods.select import get_last_user_id, get_target_data, get_user_data
from bot.database.methods.update import update_last_viewed_user
from bot.handlers.user.back_button_handler import __back_to_main_menu_manual
from bot.keyboards import KB_QUESTIONNAIRE_REVIEW
from bot.utils.main import create_user_link, decode_callback_data, get_questionnaire
from bot.database.methods.select import is_user_admin


async def get_other_questionnaire(message):
    bot = message.bot
    telegram_id = message.from_user.id
    user_data = await get_user_data(telegram_id)
    if user_data["last_viewed_user"] is None:
        last_id = random.randint(0, await get_last_user_id())
        await update_last_viewed_user(telegram_id, last_id)
        user_data["last_viewed_user"] = last_id
    
    target_data = await get_target_data(user_data, 1)
    if target_data is not None:
        try:
            if await is_user_admin(telegram_id):
                await bot.send_message(telegram_id, f"Target ID: {target_data['telegram_id']}") # to ban users who are doing something illegal
                    
            await bot.send_photo(
            telegram_id,
            caption=await get_questionnaire(target_data, 1),
            photo=str(target_data["photo_id"]),
            reply_markup=KB_QUESTIONNAIRE_REVIEW,
            parse_mode="HTML",
            )
        except:
            await bot.send_photo(
                telegram_id,
                caption=await get_questionnaire(target_data, 1),
                photo="https://pfps.gg/assets/pfps/3533-luffy-default-pfp.png",
                reply_markup=KB_QUESTIONNAIRE_REVIEW,
                parse_mode="HTML",
            )
        await update_last_viewed_user(telegram_id, target_data["id"])
        return target_data
    
    else:
        target_data = await get_target_data(user_data, 0)
        if target_data is not None:
            await update_last_viewed_user(telegram_id, 0)
            await get_other_questionnaire(message)
        else:
            await bot.send_message(
                telegram_id, "There are no people matching your filters :("
            )
            await __back_to_main_menu_manual(message)
            return None


async def send_get_questionnaire_answear(query):
    bot = query.bot
    telegram_id = query.from_user.id
    target_id = await decode_callback_data(query)

    user_data = await get_user_data(telegram_id)
    target_data = await get_user_data(target_id)

    await bot.send_message(
        telegram_id,
        f"Contact data - {await create_user_link(target_data)}\n\n<b>Telegram ID</b>: {target_data['telegram_id']}",
        parse_mode="HTML",
    )
    try:
        await bot.send_message(
            target_id,
            f"User whose replies you liked in return.\n\nContact data - {await create_user_link(user_data)}\n\n<b>Telegram ID</b>: {target_data['telegram_id']}",
            parse_mode="HTML",
        )
    except BaseException:
        pass
