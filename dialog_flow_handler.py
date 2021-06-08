import os

from google.cloud import dialogflow


def detect_intent(update, context):
    session_client = dialogflow.SessionsClient()
    session = session_client.session_path(
        project=os.getenv('DIALOG_FLOW_PROJECT_ID'),
        session=os.getenv('DIALOG_FLOW_SESSION_ID'),
    )

    text_input = dialogflow.TextInput(
        text=update.message.text,
        language_code='ru',
    )
    query_input = dialogflow.QueryInput(text=text_input)

    response = session_client.detect_intent(
        session=session,
        query_input=query_input,
    )

    update.message.reply_text(response.query_result.fulfillment_text)
