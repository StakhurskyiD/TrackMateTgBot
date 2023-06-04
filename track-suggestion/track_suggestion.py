import logging
from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove, Update
from telegram.ext import (
    CommandHandler,
    ContextTypes,
    ConversationHandler,
    MessageHandler,
    filters,
)
from TrackSuggestion.track_genres import track_genres
logger = logging.getLogger(__name__)

TRACK_GENDER, DESCRIPTION, TRACK_LINK, BIO = range(4)


def init_track_suggestion_handler():
    return ConversationHandler(
        entry_points=[MessageHandler(filters.TEXT, suggest_track)],
        states={
            TRACK_GENDER: [MessageHandler(filters.TEXT, genre)],
            DESCRIPTION: [MessageHandler(filters.TEXT, track_description), CommandHandler("skip", skip_description)],
            TRACK_LINK: [MessageHandler(filters.TEXT & ~filters.COMMAND, track_link)],
            BIO: [MessageHandler(filters.TEXT & ~filters.COMMAND, user_bio)],
        },
        fallbacks=[CommandHandler("cancel", cancel)],
    )


async def suggest_track(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    if update.message.text == 'Suggest a track':
        reply_keyboard = track_genres

        await update.message.reply_text(
            "Hi! Please choose the genre of your track",
            reply_markup=ReplyKeyboardMarkup(
                reply_keyboard, one_time_keyboard=True, input_field_placeholder="Suggest a track?"
            ),
        )

        return TRACK_GENDER


async def genre(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Stores the selected gender and asks for a photo."""
    user = update.message.from_user
    logger.info("Gender of %s: %s", user.first_name, update.message.text)
    await update.message.reply_text(
        "Greate Choice!, "
        "Please describe your composition, or send /skip if you don't want to.",
        reply_markup=ReplyKeyboardRemove(),
    )

    return DESCRIPTION


async def track_description(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Stores the photo and asks for a location."""
    user = update.message.from_user
    description = update.message.text

    # logger.info("Photo of %s: %s", user.first_name, "user_photo.jpg")
    await update.message.reply_text(
        "Gorgeous! Now, send me link for your track."
    )

    return TRACK_LINK


async def skip_description(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Skips the track description and asks for a track link."""
    user = update.message.from_user
    logger.info("User %s did not send a track description.", user.first_name)
    await update.message.reply_text(
        "I bet you look great! Now, send me your track description please, or send /skip."
    )

    return TRACK_LINK


async def track_link(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Stores the track link and asks for some info about the user."""
    user = update.message.from_user
    user_location = update.message.text

    await update.message.reply_text(
        "Maybe I can visit you sometime! At last, tell me something about yourself."
    )

    return BIO


async def user_bio(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Stores the info about the user and ends the conversation."""
    user = update.message.from_user
    logger.info("Bio of %s: %s", user.first_name, update.message.text)
    save_track_info()
    await update.message.reply_text("Thank you! I hope we can talk again some day.")
    main_menu = [
        ["Suggest a track"],
        ["Donate", "About"],
        ["Your Suggestions"]
    ]
    reply_markup = ReplyKeyboardMarkup(main_menu)

    await update.message.reply_text("Thank you for your track! Please wait for feedback", reply_markup=reply_markup)

    return ConversationHandler.END


async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Cancels and ends the conversation."""
    user = update.message.from_user
    logger.info("User %s canceled the conversation.", user.first_name)
    await update.message.reply_text(
        "Bye! I hope we can talk again some day.", reply_markup=ReplyKeyboardRemove()
    )

    return ConversationHandler.END


def save_track_info():
    print("Info is correctly saved!")