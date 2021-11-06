import logging

from telegram import Bot
from telegram.ext import CommandHandler, Filters, MessageHandler, Updater

from config import (
    TG_DIALOG_BOT_API_TOKEN,
    TG_LOGS_BOT_API_TOKEN,
    TG_USER_CHAT_ID,
)
from dialogflow_intents.detection import detect_intent
from logs_handler import TelegramLogsHandler


logger = logging.getLogger(__file__)


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

    update.message.reply_text(response_text)


if __name__ == "__main__":
    logs_bot = Bot(token=TG_LOGS_BOT_API_TOKEN)
    logger.addHandler(TelegramLogsHandler(logs_bot, TG_USER_CHAT_ID))
    logger.setLevel("INFO")

    dialog_bot = Bot(token=TG_DIALOG_BOT_API_TOKEN)
    updater = Updater(bot=dialog_bot)

    dispatcher = updater.dispatcher
    dispatcher.add_handler(CommandHandler("start", greet_user_handler))
    dispatcher.add_handler(MessageHandler(Filters.text, detect_intent_handler))

    updater.start_polling()
    updater.idle()
