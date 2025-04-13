# TODO: разбить на более понятные функции-обработчики
from pydantic import ValidationError
from telegram import Update
from telegram.ext import ContextTypes

from bot.constants import NO_HAVE_LIMITS_MSG
from bot.handlers.utilities import how_to_use, profile
from bot.keyboards.profile import profile_keyboard, back_to_profile_keyboard, remove_stats_keyboard, \
    history_pagination_keyboard
from bot.utils.statistics import generate_pie_chart
from core.database import get_db
from crud.limits import get_limits
from crud.transactions import create_transaction
from crud.users import get_user_stats, get_user_transactions
from schemas.transactions import TransactionCreate
from tools.enums import TransactionEnum


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

    elif query.data == "limits":
        db = next(get_db())
        limits = get_limits(db, update.effective_user.id)

        if not limits:
            await query.edit_message_text(
                NO_HAVE_LIMITS_MSG,
                reply_markup=back_to_profile_keyboard(),
            )
            return

        text = "📊 Ваши лимиты:\n" + "\n".join(
            f"• {limit.category_name}: {limit.amount} ₽"
            for limit in limits
        )
        await query.edit_message_text(
            text,
            reply_markup=back_to_profile_keyboard(),
        )
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

    if text == "❔ Как пользоваться?":
        await how_to_use(update, context)
        return
    if text == "👤 Профиль":
        await profile(update, context)
        return

    try:
        amount_part = text.split(maxsplit=1)[0]
        category_name = (text.split(maxsplit=1)[1]).lower()
        amount = float(amount_part)
        transaction_type = (
            TransactionEnum.income if amount > 0 else TransactionEnum.expense
        )

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
    except (IndexError, ValueError):
        await update.message.reply_text(
            "❌ Неверный формат. Пример: `-500 такси` или `+30000 зарплата`",
        )
