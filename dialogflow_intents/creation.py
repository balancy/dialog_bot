import sys

from google.api_core.exceptions import BadRequest
from google.cloud import dialogflow
import requests

from config import DIALOG_FLOW_PROJECT_ID


JSON_WITH_PHRASES = (
    "https://dvmn.org/media/filer_public/a7/db/a7db66c0-1259-4dac-9726-2d1fa9"
    "c44f20/questions.json"
)


def create_intent(
    project_id, display_name, training_phrases_parts, message_texts
):
    """Creates intent using dialogflow API.

    :param project_id: dialogflow project id
    :param display_name: name of intent
    :param training_phrases_parts: training phrases
    :param message_texts: responses to training phrases
    :return: if intent created
    """

    intents_client = dialogflow.IntentsClient()

    parent = dialogflow.AgentsClient.agent_path(project_id)
    training_phrases = []

    for training_phrases_part in training_phrases_parts:
        part = dialogflow.Intent.TrainingPhrase.Part(
            text=training_phrases_part
        )
        training_phrase = dialogflow.Intent.TrainingPhrase(parts=[part])
        training_phrases.append(training_phrase)

    text = dialogflow.Intent.Message.Text(text=message_texts)
    message = dialogflow.Intent.Message(text=text)

    intent = dialogflow.Intent(
        display_name=display_name,
        training_phrases=training_phrases,
        messages=[message],
    )

    intents_client.create_intent(request={"parent": parent, "intent": intent})


def read_data_from_json_file():
    """Reads intents from json file.

    :return: file content in structured format
    """

    response = requests.get(JSON_WITH_PHRASES)
    response.raise_for_status()

    return response.json()


if __name__ == "__main__":
    try:
        intents = read_data_from_json_file()
    except requests.exceptions.HTTPError:
        sys.exit("No json file found")

    try:
        for intent_name, intent_content in intents.items():
            create_intent(
                DIALOG_FLOW_PROJECT_ID,
                intent_name,
                intent_content["questions"],
                [intent_content["answer"]],
            )
    except BadRequest:
        sys.exit("Couldn't create intents")
