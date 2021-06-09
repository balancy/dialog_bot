import os
import sys

import google.api_core.exceptions
import requests
from dotenv import load_dotenv
from google.cloud import dialogflow

JSON_WITH_PHRASES = ("https://dvmn.org/media/filer_public/a7/db/a7db66c0-1259-"
                     "4dac-9726-2d1fa9c44f20/questions.json")


def detect_intent(text):
    """Uses dialogflow API to receive an answer to given text

    :param text: given text
    :return: answer
    """

    session_client = dialogflow.SessionsClient()
    session = session_client.session_path(
        project=os.getenv('DIALOG_FLOW_PROJECT_ID'),
        session=os.getenv('DIALOG_FLOW_SESSION_ID'),
    )

    text_input = dialogflow.TextInput(
        text=text,
        language_code='ru',
    )
    query_input = dialogflow.QueryInput(text=text_input)

    response = session_client.detect_intent(
        session=session,
        query_input=query_input,
    )

    return (response.query_result.fulfillment_text
            if bool(response.query_result.intent) else None)


def create_intent(display_name, training_phrases_parts, message_texts):
    """Creates intent using dialogflow API.

    :param display_name: name of intent
    :param training_phrases_parts: training phrases
    :param message_texts: responses to training phrases
    :return: if intent created
    """

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
        return True
    except google.api_core.exceptions.BadRequest:
        return False


def read_data_from_json_file():
    """Reads intents from json file.

    :return: file content in structured format
    """

    response = requests.get(JSON_WITH_PHRASES)
    response.raise_for_status()

    return response.json()


if __name__ == "__main__":
    load_dotenv()
    try:
        intents = read_data_from_json_file()
    except requests.exceptions.HTTPError:
        sys.exit("No json file found")

    for intent_name, intent_content in intents.items():
        create_intent(
            intent_name,
            intent_content["questions"],
            [intent_content["answer"]],
        )
