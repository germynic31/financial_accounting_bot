from telegram.ext import (
    Application,
    CallbackQueryHandler,
    CommandHandler,
    MessageHandler,
    filters,
)

from bot.handlers.limits import set_limit_command, show_limits
from bot.handlers.services import button_click, handle_message
from bot.handlers.utilities import how_to_use, profile, start
from core.config import settings


def main():
    """Функция main."""
    application = Application.builder().token(
        settings.TG_API_KEY,
    ).build()

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
