from telegram import (
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    ReplyKeyboardMarkup,
)


def profile_keyboard():
    """Возвращает клавиатуру профиля."""
    buttons = [
        [InlineKeyboardButton("📊 Статистика", callback_data="stats")],
        [InlineKeyboardButton(
            "📝 История операций", callback_data="history_1",
        )],
        [InlineKeyboardButton("🧾 Лимиты", callback_data="limits")],
    ]
    return InlineKeyboardMarkup(buttons)


def back_to_profile_keyboard():
    """Возвращает кнопку назад к профилю."""
    buttons = [
        [InlineKeyboardButton("🔙 Назад", callback_data="back_to_profile")],
    ]
    return InlineKeyboardMarkup(buttons)


def remove_stats_keyboard():
    """Возвращает кнопку убрать для статистики."""
    buttons = [
        [InlineKeyboardButton("❌ Убрать", callback_data="delete_stats")],
    ]
    return InlineKeyboardMarkup(buttons)


def history_pagination_keyboard(page: int, total_pages: int):
    """Возвращает клавиатуру пагинации."""
    buttons = [
        [
            InlineKeyboardButton("⬅️", callback_data=f"history_{page-1}"),
            InlineKeyboardButton(f"{page}/{total_pages}", callback_data=" "),
            InlineKeyboardButton("➡️", callback_data=f"history_{page+1}"),
        ],
        [InlineKeyboardButton("🔙 Назад", callback_data="back_to_profile")],
    ]
    return InlineKeyboardMarkup(buttons)


def get_main_reply_keyboard():
    """Возвращает основную клавиатуру."""
    buttons = [
        ["👤 Профиль", "❔ Как пользоваться?"],
    ]
    return ReplyKeyboardMarkup(buttons, resize_keyboard=True)
