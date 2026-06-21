from aiogram import Router, types
from database import get_user, get_user_purchases
from keyboards import back_to_menu

router = Router()

@router.callback_query(lambda c: c.data == "profile")
async def show_profile(callback: types.CallbackQuery):
    user = get_user(callback.from_user.id)
    purchases = get_user_purchases(callback.from_user.id)
    
    # Формируем список покупок
    purchases_text = "Нет активных серверов" if not purchases else ""
    for idx, p in enumerate(purchases[:5], 1):  # Показываем последние 5
        purchases_text += f"{idx}. {p['name']} ({p['country']}) - до {p['expires_at'][:10]}\n"
    
    if len(purchases) > 5:
        purchases_text += f"\n...и еще {len(purchases) - 5} серверов"
    
    text = (
        f"👤 **Ваш профиль**\n\n"
        f"🆔 ID: `{user['user_id']}`\n"
        f"👤 Имя: {user['first_name']} {user['last_name'] or ''}\n"
        f"🔗 Username: @{user['username'] or 'не указан'}\n"
        f"📅 Зарегистрирован: {user['registered_at'][:10]}\n"
        f"💰 Баланс: **{user['balance']}$**\n\n"
        f"📦 Ваши сервера:\n{purchases_text}\n"
        f"💳 Пополнить баланс: /deposit"
    )
    
    await callback.message.edit_text(text, reply_markup=back_to_menu())
    await callback.answer()
