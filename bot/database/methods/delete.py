from bot.database.main import insert_update


async def delete_user(telegram_id):
    await insert_update("DELETE FROM users WHERE telegram_id = %s", (str(telegram_id)))
