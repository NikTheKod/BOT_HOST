import sqlite3
from datetime import datetime

DB_NAME = "vps_bot.db"

def get_db():
    """Подключение к БД"""
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    """Создание таблиц при первом запуске"""
    conn = get_db()
    cursor = conn.cursor()
    
    # Таблица пользователей
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            user_id INTEGER PRIMARY KEY,
            username TEXT,
            first_name TEXT,
            last_name TEXT,
            registered_at TEXT,
            balance REAL DEFAULT 0,
            notifications INTEGER DEFAULT 1,
            language TEXT DEFAULT 'ru'
        )
    """)
    
    # Таблица серверов (каталог)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS servers (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            country TEXT,
            location TEXT,
            price REAL,
            specs TEXT,
            status TEXT DEFAULT 'available',  # available, sold
            image_url TEXT
        )
    """)
    
    # Таблица покупок
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS purchases (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            server_id INTEGER,
            purchased_at TEXT,
            expires_at TEXT,
            status TEXT DEFAULT 'active',
            FOREIGN KEY(user_id) REFERENCES users(user_id),
            FOREIGN KEY(server_id) REFERENCES servers(id)
        )
    """)
    
    # Таблица заявок в поддержку
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS support_tickets (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            message TEXT,
            status TEXT DEFAULT 'open',  # open, closed
            created_at TEXT,
            admin_answer TEXT
        )
    """)
    
    conn.commit()
    conn.close()

# --- Функции для пользователей ---

def register_user(user_id, username, first_name, last_name):
    """Регистрация нового пользователя"""
    conn = get_db()
    cursor = conn.cursor()
    
    cursor.execute("""
        INSERT OR IGNORE INTO users (user_id, username, first_name, last_name, registered_at)
        VALUES (?, ?, ?, ?, ?)
    """, (user_id, username, first_name, last_name, datetime.now().isoformat()))
    
    conn.commit()
    conn.close()

def get_user(user_id):
    """Получить данные пользователя"""
    conn = get_db()
    cursor = conn.cursor()
    user = cursor.execute("SELECT * FROM users WHERE user_id = ?", (user_id,)).fetchone()
    conn.close()
    return user

def update_user_settings(user_id, field, value):
    """Обновить настройки пользователя"""
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute(f"UPDATE users SET {field} = ? WHERE user_id = ?", (value, user_id))
    conn.commit()
    conn.close()

# --- Функции для серверов (каталог) ---

def get_all_servers():
    """Получить все сервера из каталога"""
    conn = get_db()
    cursor = conn.cursor()
    servers = cursor.execute("SELECT * FROM servers WHERE status = 'available'").fetchall()
    conn.close()
    return servers

def get_servers_by_country(country):
    """Получить сервера по стране"""
    conn = get_db()
    cursor = conn.cursor()
    servers = cursor.execute("SELECT * FROM servers WHERE country = ? AND status = 'available'", (country,)).fetchall()
    conn.close()
    return servers

def get_server(server_id):
    """Получить один сервер"""
    conn = get_db()
    cursor = conn.cursor()
    server = cursor.execute("SELECT * FROM servers WHERE id = ?", (server_id,)).fetchone()
    conn.close()
    return server

# --- Функции для покупок ---

def get_user_purchases(user_id):
    """Получить покупки пользователя"""
    conn = get_db()
    cursor = conn.cursor()
    purchases = cursor.execute("""
        SELECT s.*, p.purchased_at, p.expires_at, p.status as purchase_status
        FROM purchases p
        JOIN servers s ON p.server_id = s.id
        WHERE p.user_id = ? AND p.status = 'active'
    """, (user_id,)).fetchall()
    conn.close()
    return purchases

def add_purchase(user_id, server_id):
    """Добавить покупку (пока просто запись, без оплаты)"""
    conn = get_db()
    cursor = conn.cursor()
    
    # Помечаем сервер как проданный
    cursor.execute("UPDATE servers SET status = 'sold' WHERE id = ?", (server_id,))
    
    # Добавляем запись о покупке
    cursor.execute("""
        INSERT INTO purchases (user_id, server_id, purchased_at, expires_at)
        VALUES (?, ?, ?, ?)
    """, (user_id, server_id, datetime.now().isoformat(), datetime.now().isoformat()))
    
    conn.commit()
    conn.close()

# --- Функции для поддержки ---

def add_support_ticket(user_id, message):
    """Создать обращение в поддержку"""
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO support_tickets (user_id, message, created_at)
        VALUES (?, ?, ?)
    """, (user_id, message, datetime.now().isoformat()))
    conn.commit()
    conn.close()
