# TODO: не работают, проверить в чем проблема
from pydantic import ValidationError
from telegram import Update
from telegram.ext import ContextTypes

from bot.constants import NO_HAVE_LIMITS_MSG
from core.database import get_db
from crud.limits import get_limits, set_limit
from schemas.limits import LimitCreate


async def set_limit_command(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
):
    """Обработчик создания лимита."""
    try:
        args = context.args
        if len(args) != 2:
            raise ValueError

        category = (args[0]).lower()
        amount = float(args[1])
        limit_data = LimitCreate(
            user_id=update.effective_user.id,
            category_name=category,
            amount=amount,
        )

        db = next(get_db())
        set_limit(db, limit_data)

        await update.message.reply_text(
            f"✅ Лимит для категории «{category}» установлен: {amount} ₽",
        )
    except ValidationError as e:
        await update.message.reply_text(
            f"❌ Ошибка в данных: {e.errors()[0]['msg']}",
        )
    except (IndexError, ValueError):
        await update.message.reply_text(
            "❌ Используйте: /setlimit [категория] [сумма]\n"
            "Пример: /setlimit продукты 5000",
        )


async def show_limits(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Обработчик вывода лимита."""
    db = next(get_db())
    limits = get_limits(db, update.effective_user.id)

    if not limits:
        await update.message.reply_text(NO_HAVE_LIMITS_MSG)
        return

    text = "📊 Ваши лимиты:\n" + "\n".join(
        f"• {limit.category_name}: {limit.amount} ₽"
        for limit in limits
    )
    await update.message.reply_text(text)
