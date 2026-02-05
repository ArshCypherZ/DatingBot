from bot.database.methods.delete import delete_user
from bot.database.methods.insert import create_user
from bot.database.methods.select import get_user_data, is_user_verified
from bot.database.methods.update import update_user_phone


async def register_user(telegram_id, username):
    user_data = await get_user_data(telegram_id)
    if user_data is not None:
        if user_data["is_active"] == 0:
            await delete_user(telegram_id)
            return False
        else:
            return True
    await create_user(telegram_id, username)
    return False


async def verify_user(telegram_id, phone_number):
    if not await is_user_verified(telegram_id):
        await update_user_phone(telegram_id, phone_number)
        return True
    else:
        return False
