from aiogram import Router, types
from database import get_all_servers, get_servers_by_country, get_server, add_purchase
from keyboards import shop_categories, server_actions, back_to_menu

router = Router()

@router.callback_query(lambda c: c.data == "shop")
async def show_shop(callback: types.CallbackQuery):
    await callback.message.edit_text(
        "🛒 **Магазин VPS**\n\n"
        "Выберите страну для аренды сервера:",
        reply_markup=shop_categories()
    )
    await callback.answer()

@router.callback_query(lambda c: c.data == "shop_all")
async def show_all_servers(callback: types.CallbackQuery):
    servers = get_all_servers()
    
    if not servers:
        await callback.message.edit_text(
            "😔 К сожалению, сейчас нет свободных серверов.\n\n"
            "Попробуйте позже или свяжитесь с поддержкой.",
            reply_markup=back_to_menu()
        )
        await callback.answer()
        return
    
    # Показываем первые 5 серверов, остальные через пагинацию
    text = "📋 **Доступные сервера:**\n\n"
    for server in servers[:5]:
        text += (
            f"🏷️ **{server['name']}**\n"
            f"🌍 {server['country']}, {server['location']}\n"
            f"💻 {server['specs']}\n"
            f"💰 {server['price']}$/мес\n"
            f"🆔 ID: `{server['id']}`\n"
            f"───\n"
        )
    
    # Добавляем кнопки для каждого сервера
    from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
    from aiogram.utils.keyboard import InlineKeyboardBuilder
    
    builder = InlineKeyboardBuilder()
    for server in servers[:5]:
        builder.button(text=f"📦 {server['name']}", callback_data=f"server_{server['id']}")
    builder.button(text="🔙 Назад", callback_data="shop")
    builder.adjust(1)
    
    await callback.message.edit_text(text, reply_markup=builder.as_markup())
    await callback.answer()

@router.callback_query(lambda c: c.data.startswith("shop_country_"))
async def show_servers_by_country(callback: types.CallbackQuery):
    country = callback.data.split("_")[2]
    servers = get_servers_by_country(country)
    
    country_names = {
        "usa": "🇺🇸 США",
        "germany": "🇩🇪 Германия",
        "netherlands": "🇳🇱 Нидерланды",
        "russia": "🇷🇺 Россия"
    }
    
    if not servers:
        await callback.message.edit_text(
            f"{country_names.get(country, country)}\n\n"
            "😔 В этой стране сейчас нет свободных серверов.",
            reply_markup=back_to_menu()
        )
        await callback.answer()
        return
    
    text = f"{country_names.get(country, country)}\n\n"
    for server in servers:
        text += (
            f"🏷️ **{server['name']}**\n"
            f"📍 {server['location']}\n"
            f"💻 {server['specs']}\n"
            f"💰 {server['price']}$/мес\n"
            f"🆔 ID: `{server['id']}`\n"
            f"───\n"
        )
    
    # Кнопки для каждого сервера
    from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
    from aiogram.utils.keyboard import InlineKeyboardBuilder
    
    builder = InlineKeyboardBuilder()
    for server in servers:
        builder.button(text=f"📦 {server['name']}", callback_data=f"server_{server['id']}")
    builder.button(text="🔙 Назад", callback_data="shop")
    builder.adjust(1)
    
    await callback.message.edit_text(text, reply_markup=builder.as_markup())
    await callback.answer()

@router.callback_query(lambda c: c.data.startswith("server_"))
async def show_server_detail(callback: types.CallbackQuery):
    server_id = int(callback.data.split("_")[1])
    server = get_server(server_id)
    
    if not server or server['status'] != 'available':
        await callback.message.edit_text(
            "😔 Этот сервер уже продан или недоступен.",
            reply_markup=back_to_menu()
        )
        await callback.answer()
        return
    
    text = (
        f"🏷️ **{server['name']}**\n\n"
        f"🌍 Страна: {server['country']}\n"
        f"📍 Локация: {server['location']}\n"
        f"💻 Характеристики:\n{server['specs']}\n"
        f"💰 Цена: **{server['price']}$/мес**\n"
        f"🆔 ID: `{server['id']}`\n\n"
        f"⚠️ Внимание! Сервер активируется после оплаты.\n"
        f"🔑 Доступ к серверу вы получите в течение 5 минут."
    )
    
    await callback.message.edit_text(text, reply_markup=server_actions(server_id))
    await callback.answer()

@router.callback_query(lambda c: c.data.startswith("buy_"))
async def buy_server(callback: types.CallbackQuery):
    server_id = int(callback.data.split("_")[1])
    server = get_server(server_id)
    user = get_user(callback.from_user.id)
    
    if not server or server['status'] != 'available':
        await callback.message.edit_text(
            "❌ Этот сервер уже куплен или недоступен!",
            reply_markup=back_to_menu()
        )
        await callback.answer()
        return
    
    # Проверяем баланс
    if user['balance'] < server['price']:
        await callback.message.edit_text(
            f"❌ Недостаточно средств!\n\n"
            f"💰 Ваш баланс: {user['balance']}$\n"
            f"💳 Стоимость сервера: {server['price']}$\n\n"
            f"Пополните баланс командой /deposit",
            reply_markup=back_to_menu()
        )
        await callback.answer()
        return
    
    # Здесь в будущем будет списание денег и выдача доступа
    # Сейчас просто имитируем покупку
    add_purchase(callback.from_user.id, server_id)
    
    await callback.message.edit_text(
        f"✅ **Поздравляем!**\n\n"
        f"Вы успешно приобрели сервер **{server['name']}**!\n\n"
        f"🌍 Страна: {server['country']}\n"
        f"📍 Локация: {server['location']}\n"
        f"💻 Характеристики:\n{server['specs']}\n"
        f"💰 Сумма: {server['price']}$\n\n"
        f"🔑 Данные для доступа будут отправлены вам в течение 5 минут.\n"
        f"📩 Проверьте раздел 'Профиль' для просмотра ваших серверов.",
        reply_markup=back_to_menu()
    )
    await callback.answer("🎉 Сервер успешно куплен!")
