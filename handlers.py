def echo_message(update, context):
    """Echoing the message."""

    update.message.reply_text(update.message.text)


def greet_user(update, context):
    """Greeting user."""

    update.message.reply_text("Здравствуйте!")
