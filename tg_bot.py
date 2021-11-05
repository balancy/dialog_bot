import logging
import os

from dotenv import load_dotenv
from telegram import Bot
from telegram.ext import CommandHandler, Filters, MessageHandler, Updater

from dialogflow_intents.detection import detect_intent
from logger import get_logger


class TelegramLogsHandler(logging.Handler):
    def __init__(self, tg_bot, chat_id):
        super().__init__()
        self.chat_id = chat_id
        self.tg_bot = tg_bot

    def emit(self, record):
        log_entry = self.format(record)
        self.tg_bot.send_message(chat_id=self.chat_id, text=log_entry)


def greet_user_handler(update, context):
    """Greeting handler."""

    update.message.reply_text("Здравствуйте!")


def detect_intent_handler(update, context):
    """DialogFlow interaction handler for bot."""

    text = update.message.text
    try:
        response_text = detect_intent(text)
    except Exception as e:
        logger = get_logger(__file__)
        logger.exception(f"Что-то пошло не так: {e}")
    else:
        if response_text is not None:
            update.message.reply_text(response_text)


if __name__ == "__main__":
    load_dotenv()
    logger = get_logger(__file__)

    bot_api_token = os.getenv('TG_BOT_API_TOKEN')
    telegram_chat_id = os.getenv('TG_BOT_CHAT_ID')

    bot = Bot(token=bot_api_token)
    logger.addHandler(TelegramLogsHandler(bot, telegram_chat_id))

    updater = Updater(bot=bot)
    dispatcher = updater.dispatcher

    dispatcher.add_handler(CommandHandler("start", greet_user_handler))
    dispatcher.add_handler(MessageHandler(Filters.text, detect_intent_handler))

    updater.start_polling()
    updater.idle()
