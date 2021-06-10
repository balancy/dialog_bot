import logging

from dialogflow_intents import detect_intent

logger = logging.getLogger("tg_bot_logger")


def greet_user_handler(update, context):
    """Greeting handler."""

    update.message.reply_text("Здравствуйте!")


def detect_intent_handler(update, context):
    """DialogFlow interaction handler for bot."""

    text = update.message.text
    try:
        response_text = detect_intent(text)
    except Exception as e:
        logger.exception(f"Что-то пошло не так: {e}")
    else:
        if response_text is not None:
            update.message.reply_text(response_text)
