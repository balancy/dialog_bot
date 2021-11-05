import os
import random
import sys

from dotenv import load_dotenv
import vk_api
from vk_api.longpoll import VkLongPoll, VkEventType

from dialogflow_intents.detection import detect_intent
from logger import get_logger


def answer(event, vk_api):
    """Answer to message written in messages section in vk group.

    :param event: event when message is written
    :param vk_api: VK API
    :return: None
    """

    message = detect_intent(event.text, accept_fallback_response=False)
    if message is not None:
        vk_api.messages.send(
            user_id=event.user_id,
            message=message,
            random_id=random.randint(1, 1000),
        )


if __name__ == "__main__":
    load_dotenv()
    logger = get_logger(__file__)

    vk_session = vk_api.VkApi(token=os.getenv("VK_TOKEN"))
    vk_api = vk_session.get_api()

    longpoll = VkLongPoll(vk_session)

    try:
        for event in longpoll.listen():
            if event.type == VkEventType.MESSAGE_NEW:
                if event.to_me:
                    answer(event, vk_api)
    except KeyboardInterrupt:
        sys.exit("Работа бота прервана пользователем")
