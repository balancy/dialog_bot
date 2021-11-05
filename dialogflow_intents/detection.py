from google.cloud import dialogflow

from config import DIALOG_FLOW_PROJECT_ID, DIALOG_FLOW_SESSION_ID


def detect_intent(text, accept_fallback_response=True):
    """Uses dialogflow API to receive an answer to given text

    :param text: given text
    :param accept_fallback_response: if we react on fallback response or not
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

    if response.query_result.intent and (
        accept_fallback_response
        or (
            not response.query_result.intent.is_fallback
            and not accept_fallback_response
        )
    ):
        return response.query_result.fulfillment_text
    else:
        return None
