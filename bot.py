import asyncio
import logging
from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode

from config import BOT_TOKEN
from database import init_db
from handlers import start, profile, settings, shop, support

# Настройка логирования
logging.basicConfig(level=logging.INFO)

# Инициализация бота и диспетчера
bot = Bot(token=BOT_TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.MARKDOWN))
dp = Dispatcher()

# Подключаем роутеры
dp.include_router(start.router)
dp.include_router(profile.router)
dp.include_router(settings.router)
dp.include_router(shop.router)
dp.include_router(support.router)

async def main():
    # Инициализируем базу данных
    init_db()
    
    # Заполняем каталог тестовыми серверами (если пусто)
    from database import get_db
    conn = get_db()
    cursor = conn.cursor()
    
    # Проверяем, есть ли сервера в БД
    count = cursor.execute("SELECT COUNT(*) FROM servers").fetchone()[0]
    if count == 0:
        # Добавляем тестовые сервера
        test_servers = [
            ("VPS-USA-1", "usa", "Нью-Йорк", "4 vCPU, 8GB RAM, 100GB SSD", 5.99, "available", ""),
            ("VPS-USA-2", "usa", "Лос-Анджелес", "2 vCPU, 4GB RAM, 50GB SSD", 3.99, "available", ""),
            ("VPS-DE-1", "germany", "Франкфурт", "4 vCPU, 8GB RAM, 100GB SSD", 6.99, "available", ""),
            ("VPS-NL-1", "netherlands", "Амстердам", "6 vCPU, 16GB RAM, 200GB SSD", 7.99, "available", ""),
            ("VPS-RU-1", "russia", "Москва", "2 vCPU, 4GB RAM, 50GB SSD", 3.99, "available", ""),
            ("VPS-RU-2", "russia", "Санкт-Петербург", "4 vCPU, 8GB RAM, 100GB SSD", 4.99, "available", ""),
        ]
        
        cursor.executemany("""
            INSERT INTO servers (name, country, location, specs, price, status, image_url)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, test_servers)
        conn.commit()
        logging.info("✅ Добавлены тестовые сервера в каталог")
    
    conn.close()
    
    # Запуск бота
    logging.info("🚀 Бот запущен!")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
