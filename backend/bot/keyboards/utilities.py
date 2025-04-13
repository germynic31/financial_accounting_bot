from telegram import ReplyKeyboardMarkup


def get_main_reply_keyboard():
    """Возвращает основную клавиатуру."""
    buttons = [
        ["👤 Профиль", "❔ Как пользоваться?"],
    ]
    return ReplyKeyboardMarkup(buttons, resize_keyboard=True)