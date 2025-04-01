from io import BytesIO

import matplotlib.pyplot as plt
from crud import (
    create_transaction,
    create_user,
    get_user,
    get_user_stats,
    get_user_transactions,
)
from database import SessionLocal
from keyboards import (
    get_main_reply_keyboard,
    history_pagination_keyboard,
    profile_keyboard,
    remove_stats_keyboard,
)
from pydantic import ValidationError
from schemas import TransactionCreate, UserCreate
from telegram import Update
from telegram.ext import ContextTypes


def get_db():
    """Возвращает экземпляр сессии."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Обработчик команды старт."""
    db = next(get_db())
    user_id = update.effective_user.id
    username = update.effective_user.username

    user = get_user(db, user_id)
    if not user:
        user_data = UserCreate(telegram_id=user_id, username=username)
        create_user(db, user_data)
        await update.message.reply_text(
            "👋 Добро пожаловать в Финансовый Бот!\n"
            "Выберите действие:",
            reply_markup=get_main_reply_keyboard(),
        )
    else:
        await update.message.reply_text(
            "👋 С возвращением!\n"
            "Выберите действие:",
            reply_markup=get_main_reply_keyboard(),
        )


async def add_transaction(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Возвращает сообщение про создание операций."""
    await update.message.reply_text(
        "💸 Введите сумму и категорию в формате:\n"
        "`+30000 зарплата` (доход) или `-500 такси` (расход)",
    )


# Кнопка "Профиль"
async def generate_pie_chart(expenses: dict) -> BytesIO:
    """Генерирует "пирог" со статистикой трат."""
    labels = list(expenses.keys())
    sizes = list(expenses.values())

    fig, ax = plt.subplots()
    ax.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=90)
    ax.axis('equal')  # Круговая диаграмма

    buffer = BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)
    plt.close()
    return buffer


async def profile(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Возвращает профиль."""
    await update.message.reply_text(
        "👤 Ваш профиль",
        reply_markup=profile_keyboard(),
    )


async def button_click(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Обработчик callback'ов от кнопок."""
    query = update.callback_query
    await query.answer()

    if query.data == "back_to_profile":
        await query.edit_message_text(
            "👤 Ваш профиль",
            reply_markup=profile_keyboard(),
        )

    elif query.data == "delete_stats":
        await query.delete_message()
        return

    elif query.data == "stats":
        db = next(get_db())
        user_id = query.from_user.id
        stats = get_user_stats(db, user_id)

        chart = await generate_pie_chart(stats["expenses_by_category"])
        await context.bot.send_photo(
            chat_id=query.message.chat_id,
            photo=chart,
            caption=f"📊 Статистика:\n"
                   f"• Доходы: {stats['total_income']} ₽\n"
                   f"• Расходы: {stats['total_expense']} ₽\n"
                   f"• Баланс: {stats['balance']} ₽",
            reply_markup=remove_stats_keyboard(),
        )

    elif query.data.startswith("history_"):
        page = int(query.data.split("_")[1])
        db = next(get_db())
        user_id = query.from_user.id
        transactions = get_user_transactions(db, user_id, page=page)
        total_pages = (len(transactions) // 5 + 1)

        history_text = "📝 История операций:\n"

        for i, tx in enumerate(transactions, start=1):
            if tx.type == 'income':
                type_operation = 'пополнение'
            else:
                type_operation = 'трата'
            history_text += (
                f"{i}. {tx.created_at.strftime('%d.%m.%Y')} |"
                f" {type_operation}: {tx.amount} ₽ ({tx.category.name})\n"
            )

        await query.edit_message_text(
            history_text,
            reply_markup=history_pagination_keyboard(page, total_pages),
        )


async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Обработчик прочих сообщений."""
    db = next(get_db())
    user_id = update.effective_user.id
    text = update.message.text.strip()

    if text == "➕ Как добавить запись?":
        await add_transaction(update, context)
        return
    if text == "👤 Профиль":
        await profile(update, context)
        return

    try:
        amount_part, category_name = text.split(maxsplit=1)
        amount = float(amount_part)
        transaction_type = "income" if amount > 0 else "expense"

        transaction_data = TransactionCreate(
            amount=abs(amount),
            type=transaction_type,
            category_name=category_name,
        )
        create_transaction(db, transaction_data, user_id)
        await update.message.reply_text(
            f"✅ Добавлено: {'+' if amount > 0 else '-'}"
            f"{abs(amount)} ({category_name})",
        )
    except ValidationError as e:
        await update.message.reply_text(
            f"❌ Ошибка в данных: {e.errors()[0]['msg']}",
        )
    except ValueError:
        await update.message.reply_text(
            "❌ Неверный формат. Пример: `-500 такси` или `+30000 зарплата`",
        )
