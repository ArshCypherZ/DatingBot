from bot.database.main import select


async def is_user_registered(telegram_id):
    return len(await select(f"SELECT * FROM users WHERE telegram_id = '{telegram_id}'"))


async def get_all_users():
    return await select(f"SELECT telegram_id FROM users")


async def get_user_count():
    return list(
        (await select(f"SELECT COUNT(*) FROM users WHERE is_fake = 0"))[0].values()
    )[0]


async def get_fake_users_count():
    return list(
        (await select(f"SELECT COUNT(*) FROM users WHERE is_fake = 1"))[0].values()
    )[0]


async def get_last_user_id():
    return list((await select(f"SELECT MAX(id) FROM users"))[0].values())[0]


async def get_user_data(telegram_id):
    try:
        return (
            await select(f"SELECT * FROM users WHERE telegram_id = '{telegram_id}'")
        )[0]
    except:
        return None


async def get_user_data_by_id(id):
    try:
        return (await select(f"SELECT * FROM users WHERE id = '{id}'"))[0]
    except:
        return None


async def get_target_data(user_data, is_id_filter_on):
    try:
        if is_id_filter_on:
            return (
                await select(
                    f"SELECT * FROM users WHERE"
                    + f" gender = '{user_data['target_gender']}' AND id != '{user_data['id']}' AND id > '{user_data['last_viewed_user']}' AND id != '{user_data['last_viewed_user']}'"
                    + f" AND is_banned = '0' AND is_active = '1'"
                )
            )[0]
        else:
            return (
                await select(
                    f"SELECT * FROM users WHERE"
                    + f" gender = '{user_data['target_gender']}' AND id != '{user_data['id']}' AND id != '{user_data['last_viewed_user']}' AND is_banned = '0' AND is_active = '1'"
                )
            )[0]
    except:
        return None


async def is_user_verified(telegram_id):
    return len(
        await select(
            f"SELECT * FROM users WHERE telegram_id = {telegram_id} AND is_verified = '1'"
        )
    )


async def is_user_currently_in_support_chat(telegram_id):
    return await select(f"SELECT * FROM admin WHERE support_chat = '{telegram_id}'")


async def get_admin_data(telegram_id):
    return (await select(f"SELECT * FROM admin WHERE telegram_id = '{telegram_id}'"))[0]


async def is_user_admin(telegram_id):
    return len(await select(f"SELECT * FROM admin WHERE telegram_id = '{telegram_id}'"))


async def get_user_support_room_state(telegram_id):
    return (await select(f"SELECT * FROM users WHERE telegram_id = '{telegram_id}'"))[
        0
    ]["is_in_support_room"]


async def get_new_users_count_by_data(date):
    return list(
        (
            await select(
                f"SELECT COUNT(*) FROM users WHERE created_at BETWEEN '{date} 00:00:00' and '{date} 23:59:59' AND is_fake = 0"
            )
        )[0].values()
    )[0]


async def get_active_users_count_by_data(date):
    return list(
        (
            await select(
                f"SELECT COUNT(*) FROM users WHERE updated_at BETWEEN '{date} 00:00:00' and '{date} 23:59:59' AND is_fake = 0"
            )
        )[0].values()
    )[0]
