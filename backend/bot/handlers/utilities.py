from telegram import Update
from telegram.ext import ContextTypes

from bot.constants import HOW_TO_USE_MSG
from bot.keyboards.profile import profile_keyboard
from bot.keyboards.utilities import get_main_reply_keyboard
from core.database import get_db
from crud.users import get_user, create_user
from schemas.users import UserCreate


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


async def how_to_use(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Возвращает сообщение-гайд по боту."""
    await update.message.reply_text(HOW_TO_USE_MSG)


async def profile(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Возвращает профиль."""
    await update.message.reply_text(
        "👤 Ваш профиль",
        reply_markup=profile_keyboard(),
    )
