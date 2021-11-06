from google.cloud import dialogflow

from config import DIALOG_FLOW_PROJECT_ID, DIALOG_FLOW_SESSION_ID


def detect_intent(text):
    """Uses dialogflow API to receive an answer to given text

    :param text: given text
    :return: answer
    """

    session_client = dialogflow.SessionsClient()
    session = session_client.session_path(
        project=DIALOG_FLOW_PROJECT_ID,
        session=DIALOG_FLOW_SESSION_ID,
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

    return (
        response.query_result.intent.is_fallback,
        response.query_result.fulfillment_text,
    )
