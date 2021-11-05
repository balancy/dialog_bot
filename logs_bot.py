import logging

from telegram.bot import Bot

from config import TG_LOGS_BOT_API_TOKEN, TG_USER_CHAT_ID


logging.basicConfig(format="%(asctime)s %(levelname)s %(message)s")
logger = logging.getLogger()
logger.setLevel("INFO")


class TelegramLogsHandler(logging.Handler):
    def __init__(self, tg_bot, chat_id):
        super().__init__()
        self.chat_id = chat_id
        self.tg_bot = tg_bot

    def emit(self, record):
        log_entry = self.format(record)
        self.tg_bot.send_message(chat_id=self.chat_id, text=log_entry)


def get_logger():
    logs_bot = Bot(token=TG_LOGS_BOT_API_TOKEN)
    logger.addHandler(TelegramLogsHandler(logs_bot, TG_USER_CHAT_ID))

    return logger
