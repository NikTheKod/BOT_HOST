from aiogram import Router, types
from database import get_user, update_user_settings
from keyboards import settings_menu, back_to_menu

router = Router()

@router.callback_query(lambda c: c.data == "settings")
async def show_settings(callback: types.CallbackQuery):
    await callback.message.edit_text(
        "⚙️ **Настройки**\n\n"
        "Здесь вы можете настроить бота под себя:",
        reply_markup=settings_menu()
    )
    await callback.answer()

@router.callback_query(lambda c: c.data == "settings_notifications")
async def toggle_notifications(callback: types.CallbackQuery):
    user = get_user(callback.from_user.id)
    current = user['notifications']
    new_value = 0 if current == 1 else 1
    
    update_user_settings(callback.from_user.id, 'notifications', new_value)
    
    status = "✅ Включены" if new_value == 1 else "❌ Отключены"
    await callback.message.edit_text(
        f"🔔 **Уведомления**\n\n"
        f"Статус: {status}\n\n"
        f"Вы можете изменить настройку снова:",
        reply_markup=settings_menu()
    )
    await callback.answer(f"Уведомления {status}")

@router.callback_query(lambda c: c.data == "settings_language")
async def change_language(callback: types.CallbackQuery):
    # Простой вариант смены языка
    user = get_user(callback.from_user.id)
    current = user['language']
    new_lang = 'en' if current == 'ru' else 'ru'
    
    update_user_settings(callback.from_user.id, 'language', new_lang)
    
    lang_name = "🇷🇺 Русский" if new_lang == 'ru' else "🇬🇧 English"
    await callback.message.edit_text(
        f"🌐 **Язык**\n\n"
        f"Текущий язык: {lang_name}\n\n"
        f"Язык изменен!",
        reply_markup=settings_menu()
    )
    await callback.answer(f"Язык изменен на {lang_name}")
