import os
from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")  # Токен вашего бота
ADMIN_IDS = [123456789, 987654321]  # Ваш Telegram ID

# Цены (для отображения)
PRICES = {
    "usa": 5.99,
    "germany": 6.99,
    "netherlands": 7.99,
    "russia": 3.99,
}
