from bot.database.main import insert_update


async def create_user(telegram_id, username):
    if username is not None:
        await insert_update(
            "INSERT INTO users (telegram_id, username) VALUES (%s, %s)",
            (str(telegram_id), str(username)),
        )
    else:
        await insert_update(
            "INSERT INTO users (telegram_id) VALUES (%s)", (str(telegram_id))
        )


async def create_fake_user(telegram_id):
    await insert_update(
        "INSERT INTO users (telegram_id, is_fake) VALUES (%s, 1)", (str(telegram_id))
    )


async def set_user_admin_role(telegram_id, role):
    await insert_update(
        "INSERT INTO admin (telegram_id, role) VALUES (%s, %s)",
        (str(telegram_id), str(role)),
    )
