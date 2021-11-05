import os
import random

from dotenv import load_dotenv
import vk_api
from vk_api.longpoll import VkLongPoll, VkEventType

from logs_bot import get_logger
from dialogflow_intents.detection import detect_intent


logger = get_logger()


def answer(event, vk_api):
    """Answer to message written in messages section in vk group.

    :param event: event when message is written
    :param vk_api: VK API
    :return: None
    """

    text = event.text
    user_id = event.user_id

    logger.info(f"Received \"{text}\" from id{user_id} in VK")
    message = detect_intent(text, accept_fallback_response=False)

    if message is not None:
        logger.info(f"Responded \"{message}\" to id{user_id} in VK")
        vk_api.messages.send(
            user_id=user_id,
            message=message,
            random_id=random.randint(1, 1000),
        )


if __name__ == "__main__":
    load_dotenv()

    vk_session = vk_api.VkApi(token=os.getenv("VK_TOKEN"))
    vk_api = vk_session.get_api()

    longpoll = VkLongPoll(vk_session)

    for event in longpoll.listen():
        if event.type == VkEventType.MESSAGE_NEW:
            if event.to_me:
                answer(event, vk_api)
