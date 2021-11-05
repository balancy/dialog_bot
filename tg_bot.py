import os

from dotenv import load_dotenv
from telegram import Bot
from telegram.ext import CommandHandler, Filters, MessageHandler, Updater

from dialogflow_intents.detection import detect_intent
from logs_bot import get_logger


logger = get_logger()


def greet_user_handler(update, context):
    """Greeting handler."""

    update.message.reply_text("Здравствуйте!")


def detect_intent_handler(update, context):
    """DialogFlow interaction handler for bot."""

    username = update.message.from_user.username
    text = update.message.text
    logger.info(f"Received \"{text}\" from {username} in telegram")

    response_text = detect_intent(text)
    logger.info(f"Responded \"{response_text}\" to {username} in telegram")

    if response_text is not None:
        update.message.reply_text(response_text)


if __name__ == "__main__":
    load_dotenv()

    tg_dialog_bot_api_token = os.getenv('TG_DIALOG_BOT_API_TOKEN')
    dialog_bot = Bot(token=tg_dialog_bot_api_token)

    updater = Updater(bot=dialog_bot)
    dispatcher = updater.dispatcher

    dispatcher.add_handler(CommandHandler("start", greet_user_handler))
    dispatcher.add_handler(MessageHandler(Filters.text, detect_intent_handler))

    updater.start_polling()
    updater.idle()
