import os

import google.api_core.exceptions
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


def create_intent(display_name, training_phrases_parts, message_texts):
    intents_client = dialogflow.IntentsClient()

    parent = dialogflow.AgentsClient.agent_path(
        os.getenv('DIALOG_FLOW_PROJECT_ID')
    )
    training_phrases = []

    for training_phrases_part in training_phrases_parts:
        part = dialogflow.Intent.TrainingPhrase.Part(text=training_phrases_part)
        training_phrase = dialogflow.Intent.TrainingPhrase(parts=[part])
        training_phrases.append(training_phrase)

    text = dialogflow.Intent.Message.Text(text=message_texts)
    message = dialogflow.Intent.Message(text=text)

    intent = dialogflow.Intent(
        display_name=display_name,
        training_phrases=training_phrases,
        messages=[message],
    )

    try:
        intents_client.create_intent(
            request={"parent": parent, "intent": intent}
        )
    except google.api_core.exceptions.BadRequest:
        # intent already exists with this display name
        pass
    return
