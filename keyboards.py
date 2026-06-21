from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder

def main_menu():
    """Главное меню"""
    builder = InlineKeyboardBuilder()
    builder.button(text="👤 Профиль", callback_data="profile")
    builder.button(text="🛒 Магазин", callback_data="shop")
    builder.button(text="⚙️ Настройки", callback_data="settings")
    builder.button(text="💬 Поддержка", callback_data="support")
    builder.adjust(2)
    return builder.as_markup()

def back_to_menu():
    """Кнопка назад в главное меню"""
    builder = InlineKeyboardBuilder()
    builder.button(text="🔙 Назад", callback_data="main_menu")
    return builder.as_markup()

def shop_categories():
    """Категории магазина"""
    builder = InlineKeyboardBuilder()
    builder.button(text="🌍 Все сервера", callback_data="shop_all")
    builder.button(text="🇺🇸 США", callback_data="shop_country_usa")
    builder.button(text="🇩🇪 Германия", callback_data="shop_country_germany")
    builder.button(text="🇳🇱 Нидерланды", callback_data="shop_country_netherlands")
    builder.button(text="🇷🇺 Россия", callback_data="shop_country_russia")
    builder.button(text="🔙 Назад", callback_data="main_menu")
    builder.adjust(2)
    return builder.as_markup()

def server_actions(server_id):
    """Действия с конкретным сервером"""
    builder = InlineKeyboardBuilder()
    builder.button(text="💳 Купить", callback_data=f"buy_{server_id}")
    builder.button(text="🔙 Назад", callback_data="shop")
    builder.adjust(1)
    return builder.as_markup()

def settings_menu():
    """Меню настроек"""
    builder = InlineKeyboardBuilder()
    builder.button(text="🔔 Уведомления", callback_data="settings_notifications")
    builder.button(text="🌐 Язык", callback_data="settings_language")
    builder.button(text="🔙 Назад", callback_data="main_menu")
    builder.adjust(1)
    return builder.as_markup()

def support_menu():
    """Меню поддержки"""
    builder = InlineKeyboardBuilder()
    builder.button(text="📝 Написать в поддержку", callback_data="support_write")
    builder.button(text="❓ Частые вопросы", callback_data="support_faq")
    builder.button(text="🔙 Назад", callback_data="main_menu")
    builder.adjust(1)
    return builder.as_markup()
