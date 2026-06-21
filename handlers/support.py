from aiogram import Router, types
from aiogram.filters import Command
from database import add_support_ticket
from keyboards import support_menu, back_to_menu

router = Router()

@router.callback_query(lambda c: c.data == "support")
async def show_support(callback: types.CallbackQuery):
    await callback.message.edit_text(
        "💬 **Поддержка**\n\n"
        "Здесь вы можете:\n"
        "• Задать вопрос\n"
        "• Сообщить о проблеме\n"
        "• Получить помощь\n\n"
        "Напишите нам, и мы ответим в ближайшее время!",
        reply_markup=support_menu()
    )
    await callback.answer()

@router.callback_query(lambda c: c.data == "support_write")
async def support_write(callback: types.CallbackQuery):
    await callback.message.edit_text(
        "✍️ **Написать в поддержку**\n\n"
        "Просто отправьте сообщение текстом.\n"
        "Мы ответим вам в ближайшее время.\n\n"
        "_(Для отмены напишите /cancel)_",
        reply_markup=back_to_menu()
    )
    await callback.answer()
    
    # Устанавливаем состояние ожидания сообщения
    # (для простоты пропустим FSM, просто принимаем следующее сообщение)

@router.message(Command("support"))
async def support_command(message: types.Message):
    await message.answer(
        "💬 Поддержка\n\nНапишите ваше сообщение, и мы ответим вам.",
        reply_markup=back_to_menu()
    )

# Обработка текстовых сообщений в поддержку
@router.message()
async def handle_support_message(message: types.Message):
    # Простая логика: если сообщение не команда и не callback
    if message.text and not message.text.startswith('/'):
        # Сохраняем заявку
        add_support_ticket(message.from_user.id, message.text)
        
        await message.answer(
            "✅ Ваше сообщение отправлено в поддержку!\n\n"
            "Мы ответим вам в ближайшее время.\n"
            "Спасибо за обращение! 🙏",
            reply_markup=back_to_menu()
        )
        
        # Уведомление админам
        from config import ADMIN_IDS
        from aiogram import Bot
        from config import BOT_TOKEN
        
        bot = Bot(token=BOT_TOKEN)
        for admin_id in ADMIN_IDS:
            await bot.send_message(
                admin_id,
                f"📩 Новое обращение в поддержку!\n\n"
                f"👤 От: @{message.from_user.username or message.from_user.first_name}\n"
                f"🆔 ID: {message.from_user.id}\n"
                f"💬 Сообщение:\n{message.text}"
            )

@router.callback_query(lambda c: c.data == "support_faq")
async def support_faq(callback: types.CallbackQuery):
    text = (
        "❓ **Частые вопросы**\n\n"
        "**1. Как купить сервер?**\n"
        "Перейдите в 'Магазин', выберите сервер и нажмите 'Купить'.\n\n"
        "**2. Как пополнить баланс?**\n"
        "Используйте команду /deposit\n\n"
        "**3. Как получить доступ к серверу?**\n"
        "После покупки данные появятся в вашем профиле.\n\n"
        "**4. Что делать, если сервер не работает?**\n"
        "Напишите в поддержку, мы поможем.\n\n"
        "**5. Можно ли продлить сервер?**\n"
        "Да, продление доступно в профиле за 7 дней до истечения.\n\n"
        "Остались вопросы? Напишите нам!"
    )
    await callback.message.edit_text(text, reply_markup=support_menu())
    await callback.answer()
