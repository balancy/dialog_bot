import sys

from dotenv import load_dotenv
import requests

from intent_handlers import create_intent

JSON_WITH_PHRASES = ("https://dvmn.org/media/filer_public/a7/db/a7db66c0-1259-"
                     "4dac-9726-2d1fa9c44f20/questions.json")


def read_intents_from_json():
    response = requests.get(JSON_WITH_PHRASES)
    response.raise_for_status()

    return response.json()


if __name__ == "__main__":
    load_dotenv()
    try:
        intents = read_intents_from_json()
    except requests.exceptions.HTTPError:
        sys.exit("No json file found")

    for intent_name, intent_content in intents.items():
        create_intent(
            intent_name,
            intent_content["questions"],
            [intent_content["answer"]],
        )
