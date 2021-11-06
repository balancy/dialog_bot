import argparse
import json
import sys
import traceback

from google.api_core.exceptions import BadRequest
from google.cloud import dialogflow
import requests

from config import DIALOG_FLOW_PROJECT_ID, JSON_WITH_PHRASES


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


def read_data_from_json_file(url):
    """Reads intents from json file.

    :param url: url to JSON file
    :return: file content in structured format
    """

    response = requests.get(url)
    response.raise_for_status()

    return response.json()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description=(
            'Create dialogflow intents based on the JSON file from given url.'
        )
    )
    parser.add_argument(
        "-u",
        "--url",
        type=str,
        default=JSON_WITH_PHRASES,
        help="url to the JSON file",
    )
    args = parser.parse_args()
    url = args.url

    try:
        intents = read_data_from_json_file(url)
    except requests.exceptions.HTTPError:
        sys.exit(f"Url \"{url}\" isn't found. Check if it's correct.")
    except json.decoder.JSONDecodeError:
        sys.exit(f"No JSON file found on url \"{url}\"")

    for intent_name, intent_content in intents.items():
        try:
            create_intent(
                DIALOG_FLOW_PROJECT_ID,
                intent_name,
                intent_content["questions"],
                [intent_content["answer"]],
            )
        except:
            print(
                f"It's not possible to create intent \"{intent_name}\". "
                "Maybe it's already created."
            )
