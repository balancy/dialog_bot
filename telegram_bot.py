import os

from dotenv import load_dotenv
from telegram.ext import CommandHandler, Filters, MessageHandler, Updater

from bot_handlers import detect_intent_handler
from bot_handlers import  greet_user_handler

if __name__ == "__main__":
    load_dotenv()
    BOT_API_TOKEN = os.getenv('BOT_API_TOKEN')

    updater = Updater(BOT_API_TOKEN)
    dispatcher = updater.dispatcher

    dispatcher.add_handler(CommandHandler("start", greet_user_handler))
    dispatcher.add_handler(MessageHandler(Filters.text, detect_intent_handler))

    updater.start_polling()
    updater.idle()
