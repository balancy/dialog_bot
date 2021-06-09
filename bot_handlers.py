from dialogflow_intents import detect_intent


def greet_user_handler(update, context):
    """Greeting user."""

    update.message.reply_text("Здравствуйте!")


def detect_intent_handler(update, context):
    text = update.message.text
    response_text = detect_intent(text)
    if not response_text is None:
        update.message.reply_text(response_text)