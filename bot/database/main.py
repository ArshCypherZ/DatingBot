import os

import aiomysql
from dotenv import load_dotenv

load_dotenv()

DB = os.getenv("DB_NAME")
HOST = os.getenv("DB_HOST")
USER = os.getenv("DB_USER")
PASSWORD = os.getenv("DB_PASSWORD")


async def open_connection():
    database = await aiomysql.connect(
        host=HOST, port=3306, user=USER, password=PASSWORD, db=DB
    )
    return database


async def select(sql):
    database = await open_connection()
    cursor = await database.cursor(aiomysql.DictCursor)
    await cursor.execute(sql)
    result = await cursor.fetchall()
    await cursor.close()
    database.close()
    return result


async def insert_update(sql, val):
    database = await open_connection()
    cursor = await database.cursor()
    await cursor.execute(sql, val)
    await database.commit()
    await cursor.close()
    database.close()


async def create_admin_table():
    database = await open_connection()
    cursor = await database.cursor()
    await cursor.execute(create_admin_tables)
    await database.commit()
    await cursor.close()
    database.close()


async def create_user_table():
    database = await open_connection()
    cursor = await database.cursor()
    await cursor.execute(create_users_table)
    await database.commit()
    await cursor.close()
    database.close()


create_users_table = """
CREATE TABLE users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    telegram_id BIGINT,
    username VARCHAR(255),
    is_fake BOOLEAN DEFAULT 0,
    age INT,
    gender VARCHAR(255),
    is_banned BOOLEAN DEFAULT 0,
    city VARCHAR(255),
    created_at DATETIME,
    updated_at DATETIME,
    is_active BOOLEAN DEFAULT 1,
    phone_number VARCHAR(255),
    is_verified BOOLEAN DEFAULT 0,
    instagram VARCHAR(255),
    name VARCHAR(255),
    photo_id VARCHAR(255),
    description VARCHAR(255),
    target_gender VARCHAR(255),
    last_viewed_user BIGINT,
    latitude FLOAT,
    longitude FLOAT,
    is_in_support_room BOOLEAN DEFAULT 0

);
"""

create_admin_tables = """
CREATE TABLE admin (
    id INT AUTO_INCREMENT PRIMARY KEY,
    telegram_id BIGINT,
    role VARCHAR(255),
    support_chat VARCHAR(255)
);
"""
