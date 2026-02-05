<h1 align="center">💘 Dating Bot</h1>

<p align="center">
    <a href="https://github.com/ArshCypherZ">
        <img src="https://img.shields.io/badge/Status-Maintained-blue?style=for-the-badge&logo=telegram" alt="Status" />
    </a>
    <a href="https://python.org">
        <img src="https://img.shields.io/badge/Python-3.10%2B-yellow?style=for-the-badge&logo=python" alt="Python" />
    </a>
    <a href="https://aiogram.dev">
        <img src="https://img.shields.io/badge/Aiogram-2.x-blue?style=for-the-badge&logo=telegram" alt="Aiogram" />
    </a>
</p>

<p align="center">
  <b>An advanced, anonymous dating bot for Telegram.</b>
  <br>
  <i>Match, Chat, and Connect with people nearby.</i>
</p>

<p align="center">
    <a href="https://railway.app/new">
        <img src="https://railway.app/button.svg" alt="Deploy on Railway">
    </a>
</p>

---

## Features

- Find partners based on gender preference.
- Location-based matching.
- Spam Protection

---

## Deployment

### Option 1: One-Click Deploy (Recommended)

You can easily deploy this bot on **Railway**, **Zeabur**, or **Render**.

1. **Fork this repository**.
2. Click the **Deploy on Railway** button above.
3. Set the required [Environment Variables](#-configuration).
4. Connect a MySQL service (Railway provides this with one click).

### Option 2: Docker (Self-Hosted)

Run the bot anywhere with Docker Compose.

```bash
# 1. Clone the repo
git clone https://github.com/ArshCypherZ/DatingBot.git
cd DatingBot

# 2. Configure environment
cp .env.example .env
nano .env  # Fill in your BOT_TOKEN and DB credentials

# 3. Run
docker-compose up -d --build
```

### Option 3: Local Development

```bash
# Install dependencies
pip install -r requirements.txt

# Configure .env file
# (See Configuration section below)

# Run the bot
python run.py
```

---

## Configuration

Create a `.env` file in the root directory:

```properties
# Telegram Bot Token (Get from @BotFather)
BOT_TOKEN=123456789:ABCdefGHIjklMNOpqrSTUvwxYZ

# Admin ID (For admin panel access)
ADMIN_CHAT_ID=123456789

# Database Configuration
DB_NAME=datingbot
DB_HOST=localhost
DB_USER=datingbot
DB_PASSWORD=your_secure_password
```

---

## Support

Reach out to the **Spiral Tech Division** for support or custom bot development.

<p align="center">
    <a href="https://t.me/SpiralTechDivision">
        <img src="https://img.shields.io/badge/Contact-Developer-blue?style=flat&logo=telegram" alt="Contact Developer" />
    </a>
</p>

---

<p align="center">
    Made with ❤️ by <a href="https://github.com/ArshCypherZ">ArshCypherZ</a>
</p>
