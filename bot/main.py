import os

from dotenv import load_dotenv
from telegram.ext import (
    Application,
    CallbackQueryHandler,
    CommandHandler,
    MessageHandler,
    filters,
)

from database import init_db
from handlers import (
    add_transaction,
    button_click,
    handle_message,
    profile,
    start,
)

load_dotenv()


async def post_init(app: Application):
    """Создает базу данных при запуске."""
    init_db()


def main():
    """Функция main."""
    application = Application.builder().token(
        os.getenv("TG_TOKEN"),
    ).post_init(post_init).build()

    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("add", add_transaction))
    application.add_handler(CommandHandler("profile", profile))
    application.add_handler(CallbackQueryHandler(button_click))
    application.add_handler(
        MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message),
    )

    application.run_polling()


if __name__ == "__main__":
    main()
