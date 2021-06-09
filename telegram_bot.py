import logging
import os

from dotenv import load_dotenv
from telegram import Bot
from telegram.ext import CommandHandler, Filters, MessageHandler, Updater

from bot_handlers import detect_intent_handler
from bot_handlers import greet_user_handler

logger = logging.getLogger("tg_bot_logger")


class TelegramLogsHandler(logging.Handler):
    def __init__(self, tg_bot, chat_id):
        super().__init__()
        self.chat_id = chat_id
        self.tg_bot = tg_bot

    def emit(self, record):
        log_entry = self.format(record)
        self.tg_bot.send_message(chat_id=self.chat_id, text=log_entry)


if __name__ == "__main__":
    logging.basicConfig(format="%(process)d %(levelname)s %(message)s")
    logger.setLevel(logging.INFO)

    load_dotenv()
    bot_api_token = os.getenv('TG_BOT_API_TOKEN')
    telegram_chat_id = os.getenv('TG_BOT_CHAT_ID')

    bot = Bot(token=bot_api_token)
    logger.addHandler(TelegramLogsHandler(bot, telegram_chat_id))

    updater = Updater(bot=bot)
    dispatcher = updater.dispatcher

    dispatcher.add_handler(CommandHandler("start", greet_user_handler))
    dispatcher.add_handler(MessageHandler(Filters.text, detect_intent_handler))

    try:
        updater.start_polling()
    except Exception as e:
        logger.warning("Что-то пошло не так: ", e)
    updater.idle()
