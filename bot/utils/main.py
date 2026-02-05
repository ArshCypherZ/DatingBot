import json
import logging
import re

from aiogram import types
from aiogram.utils.exceptions import MessageCantBeDeleted, MessageToDeleteNotFound
from fuzzywuzzy import fuzz


def load_city_data_from_file(file_path):
    with open(file_path, "r") as file:
        city_data = json.load(file)
    return city_data


async def decode_callback_data(callback):
    return callback.data.split("_")[1]


async def get_location_by_coordinates(latitude, longitude):
    city_data = load_city_data_from_file("city.json")
    for city_name, details in city_data.items():
        if details["latitude"] == latitude and details["longitude"] == longitude:
            return await form_location_data(details["city"])
    return f"No city found for the given coordinates ({latitude}, {longitude})."


async def get_location_by_name(city):
    city_data = load_city_data_from_file("city.json")
    best_match = None
    best_ratio = 0

    for city_name, details in city_data.items():
        ratio = fuzz.ratio(city.lower(), city_name.lower())
        if ratio > best_ratio:
            best_ratio = ratio
            best_match = city_name

    if best_match is not None:
        return await form_location_data(city_data[best_match])
    else:
        return "not found"


async def form_location_data(location_data):
    if isinstance(location_data, dict):
        return (
            f"{location_data.get('accentcity', location_data.get('city'))}\n"
            f"Region: {location_data.get('region')}\n"
            f"Population: {location_data.get('population')}\n"
            f"Lat: {location_data.get('latitude')}\n"
            f"Long: {location_data.get('longitude')}"
        )
    return location_data


async def add_age_ending(age):
    age = str(age)
    if age[1] == "1":
        return age + "year"
    elif age[1] == "2" or age[1] == "3" or age[1] == "4":
        return age + "years"
    else:
        return age + "years"


async def add_age_filter_ending(age):
    age = str(age)
    if age[1] == "1":
        return age + " year"
    else:
        return age + "years"


async def get_instagram_status(instagram):
    if instagram is None:
        return "User has not attached Instagram"
    else:
        return f'<a href="https://www.instagram.com/{instagram}/">@{instagram}</a>'


async def get_questionnaire_status(status):
    if status:
        return "Confirmed"
    else:
        return "Unconfirmed"


async def get_questionnaire(user_data, questionnaire_type):
    if questionnaire_type == 1:
        return f"🌆 {user_data['name']}, {await add_age_ending(user_data['age'])}, {user_data['city']}\n\nAbout myself - {user_data['description']}\n\nInstagram - {await get_instagram_status(user_data['instagram'])}\nQuestionnaire status - {await get_questionnaire_status(user_data['is_verified'])}"
    elif questionnaire_type == 0:
        return f"🌆 {user_data['name']}, {await add_age_ending(user_data['age'])}, {user_data['city']}\n\nAbout myself - {user_data['description']}"
    elif questionnaire_type == 2:
        return (
            f"This user is interested in you!\n\n🌆 {user_data['name']}, {await add_age_ending(user_data['age'])},"
            + f" {user_data['city']}\n\nAbout myself - {user_data['description']}\n\n"
            + f"Instagram - {await get_instagram_status(user_data['instagram'])}\nQuestionnaire status - {await get_questionnaire_status(user_data['is_verified'])}"
        )


def delete_old_message(func):
    async def inner_function(*args):
        try:
            callback_query = args[0]
            # Try to get message from callback query or arguments
            message = getattr(callback_query, 'message', None)
            if not message and isinstance(callback_query, types.Message):
                message = callback_query
            
            if message:
                await message.delete()
        except (AttributeError, MessageToDeleteNotFound, MessageCantBeDeleted) as e:
            # logging.warning(f"Message deletion failed: {e}")
            pass
        except Exception as e:
            logging.warning(e)
        
        await func(*args)

    return inner_function


async def validate_instagram(instagram):
    if re.search(
        "(?:(?:http|https):\\/\\/)?(?:www.)?(?:instagram.com|instagr.am|instagr.com)\\/(\\w+ )",
        instagram,
    ):
        instagram = instagram.split("/")
        return instagram[3]
    elif instagram[0] == "@":
        return instagram[1:]
    return False


async def format_filters_data(user_data):
    formatted_data = []
    if user_data["target_gender"] == "male":
        formatted_data.append("Male")
    else:
        formatted_data.append("Woman")
    return formatted_data


async def create_user_link(user_data):
    if user_data["username"] is not None:
        return f'<a href="https://t.me/{user_data["username"]}">{user_data["name"]}</a>'
    else:
        return (
            f'<a href="tg://user?id={user_data["telegram_id"]}">{user_data["name"]}</a>'
        )
