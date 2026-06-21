from aiogram import Router, types
from aiogram.filters import Command
from database import register_user, get_user
from keyboards import main_menu

router = Router()

@router.message(Command("start"))
async def cmd_start(message: types.Message):
    user_id = message.from_user.id
    username = message.from_user.username
    first_name = message.from_user.first_name
    last_name = message.from_user.last_name
    
    # Регистрируем пользователя
    register_user(user_id, username, first_name, last_name)
    
    user = get_user(user_id)
    
    await message.answer(
        f"👋 Привет, {first_name}!\n\n"
        "Добро пожаловать в VPS Shop Bot! 🚀\n"
        "Здесь вы можете арендовать VPS сервера по выгодным ценам.\n\n"
        f"💰 Ваш баланс: {user['balance']}$\n\n"
        "Выберите действие в меню ниже:",
        reply_markup=main_menu()
    )

@router.callback_query(lambda c: c.data == "main_menu")
async def back_to_main(callback: types.CallbackQuery):
    user = get_user(callback.from_user.id)
    await callback.message.edit_text(
        f"🏠 Главное меню\n\n"
        f"💰 Ваш баланс: {user['balance']}$",
        reply_markup=main_menu()
    )
    await callback.answer()
