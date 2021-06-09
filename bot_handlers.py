from dialogflow_intents import detect_intent


def greet_user_handler(update, context):
    """Greeting handler."""

    update.message.reply_text("Здравствуйте!")


def detect_intent_handler(update, context):
    """DialogFlow interaction handler for bot."""

    text = update.message.text
    response_text = detect_intent(text)
    if response_text is not None:
        update.message.reply_text(response_text)
