from core.config import settings
from database import init_db
from handlers import (
    button_click,
    handle_message,
    how_to_use,
    profile,
    set_limit_command,
    show_limits,
    start,
)
from telegram.ext import (
    Application,
    CallbackQueryHandler,
    CommandHandler,
    MessageHandler,
    filters,
)


async def post_init(app: Application):
    """Создает базу данных при запуске."""
    init_db()


def main():
    """Функция main."""
    application = Application.builder().token(
        settings.API_KEY,
    ).post_init(post_init).build()

    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("how_to_use", how_to_use))
    application.add_handler(CommandHandler("profile", profile))
    application.add_handler(CommandHandler("setlimit", set_limit_command))
    application.add_handler(CommandHandler("limits", show_limits))
    application.add_handler(CallbackQueryHandler(button_click))
    application.add_handler(
        MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message),
    )

    application.run_polling()


if __name__ == "__main__":
    main()
