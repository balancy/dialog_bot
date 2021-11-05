import logging
import os

from dotenv import load_dotenv
from telegram.bot import Bot


logging.basicConfig(format="%(asctime)s %(levelname)s %(message)s")
logger = logging.getLogger()
logger.setLevel("INFO")

load_dotenv()


class TelegramLogsHandler(logging.Handler):
    def __init__(self, tg_bot, chat_id):
        super().__init__()
        self.chat_id = chat_id
        self.tg_bot = tg_bot

    def emit(self, record):
        log_entry = self.format(record)
        self.tg_bot.send_message(chat_id=self.chat_id, text=log_entry)


def get_logger():
    tg_user_id = os.getenv('TG_USER_CHAT_ID')
    tg_logs_bot_api_token = os.getenv('TG_LOGS_BOT_API_TOKEN')

    logs_bot = Bot(token=tg_logs_bot_api_token)
    logger.addHandler(TelegramLogsHandler(logs_bot, tg_user_id))

    return logger
