from bot.database.main import insert_update


async def update_user_phone(telegram_id, phone_number):
    await insert_update(
        "UPDATE users SET phone_number = %s, is_verified = '1' WHERE telegram_id = %s",
        (str(phone_number), str(telegram_id)),
    )


async def update_user_instagram(telegram_id, instagram):
    await insert_update(
        "UPDATE users SET instagram = %s, is_verified = '1' WHERE telegram_id = %s",
        (str(instagram), str(telegram_id)),
    )


async def update_user_name(telegram_id, name):
    await insert_update(
        "UPDATE users SET name = %s WHERE telegram_id = %s",
        (str(name), str(telegram_id)),
    )


async def update_user_gender(telegram_id, gender):
    await insert_update(
        "UPDATE users SET gender = %s WHERE telegram_id = %s",
        (str(gender), str(telegram_id)),
    )


async def update_user_age(telegram_id, age):
    await insert_update(
        "UPDATE users SET age = %s WHERE telegram_id = %s", (str(age), str(telegram_id))
    )


async def update_user_location(telegram_id, location):
    try:
        await insert_update(
        "UPDATE users SET city = %s WHERE telegram_id = %s",
        (str(location["city"]), str(telegram_id)),
        )
    except:
        await insert_update(
            "UPDATE users SET city = %s WHERE telegram_id = %s",
            (str(location), str(telegram_id)),
        )


async def update_user_photo(telegram_id, photo):
    await insert_update(
        "UPDATE users SET photo_id = %s WHERE telegram_id = %s",
        (str(photo), str(telegram_id)),
    )


async def update_user_description(telegram_id, description):
    await insert_update(
        "UPDATE users SET description = %s WHERE telegram_id = %s",
        (str(description), str(telegram_id)),
    )


async def update_target_gender(telegram_id, target_gender):
    await insert_update(
        "UPDATE users SET target_gender = %s WHERE telegram_id = %s",
        (str(target_gender), str(telegram_id)),
    )


async def update_account_active_status(telegram_id, status):
    await insert_update(
        "UPDATE users SET is_active = %s WHERE telegram_id = %s",
        (str(status), str(telegram_id)),
    )



async def update_all_unregistered_active_status(status):
    await insert_update(
        "UPDATE users SET is_active = %s WHERE is_active = 0", (str(status))
    )


async def update_last_viewed_user(telegram_id, id):
    await insert_update(
        "UPDATE users SET last_viewed_user = %s WHERE telegram_id = %s",
        (str(id), str(telegram_id)),
    )


async def update_admin_support_chat_state(telegram_id, chat):
    await insert_update(
        "UPDATE admin SET support_chat = %s WHERE telegram_id = %s",
        (chat, str(telegram_id)),
    )


async def update_user_support_state(telegram_id, state):
    await insert_update(
        "UPDATE users SET is_in_support_room = %s WHERE telegram_id = %s",
        (str(state), str(telegram_id)),
    )


async def update_user_last_active_time(telegram_id):
    await insert_update(
        "UPDATE users SET updated_at = CURRENT_TIMESTAMP WHERE telegram_id = %s",
        (str(telegram_id)),
    )


async def update_user_ban_state(telegram_id, state):
    await insert_update(
        "UPDATE users SET is_banned = %s WHERE telegram_id = %s",
        (str(state), str(telegram_id)),
    )


async def update_user_coordinates(telegram_id, latitude, longitude):
    await insert_update(
        "UPDATE users SET latitude = %s, longitude = %s WHERE telegram_id = %s",
        (str(latitude), str(longitude), str(telegram_id)),
    )
