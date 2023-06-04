import logging
import os

from dotenv import load_dotenv
from telegram import __version__ as TG_VER

from TrackSuggestion.track_suggestion import init_track_suggestion_handler

try:
    from telegram import __version_info__
except ImportError:
    __version_info__ = (0, 0, 0, 0, 0)  # type: ignore[assignment]

if __version_info__ < (20, 0, 0, "alpha", 5):
    raise RuntimeError(
        f"This example is not compatible with your current PTB version {TG_VER}. To view the "
        f"{TG_VER} version of this example, "
    )
from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove, Update
from telegram.ext import (
    Application,
    CommandHandler,
    ContextTypes,
    ConversationHandler,
    MessageHandler,
    filters,
)

# Enable logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logger = logging.getLogger(__name__)


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    main_menu = [
        ["Suggest a track"],
        ["Donate", "About"],
        ["Your Suggestions"]
    ]
    reply_markup = ReplyKeyboardMarkup(main_menu)

    await update.message.reply_text("Please choose:", reply_markup=reply_markup)


async def donate(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:

    await update.message.reply_text("Please choose:")


async def about(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:

    await update.message.reply_text("Please choose:")


async def user_suggestions(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:

    await update.message.reply_text("Please choose:")


def main() -> None:
    """Run the bot."""
    # Create the Application and pass it your bot's token.
    application = Application.builder().token(os.getenv('BOT_TOKEN')).build()

    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("donate", donate))
    application.add_handler(CommandHandler("about", about))
    application.add_handler(CommandHandler("leave_suggestion", user_suggestions))

    application.add_handler(init_track_suggestion_handler())

    # Run the bot until the user presses Ctrl-C
    application.run_polling()


load_dotenv()  # take environment variables from .env.

if __name__ == "__main__":
    main()