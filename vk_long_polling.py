import logging
import os
import random

from dotenv import load_dotenv
import vk_api
from vk_api.longpoll import VkLongPoll, VkEventType

from dialogflow_intents import detect_intent


def answer(event, vk_api):
    """Answer to message written in messages section in vk group.

    :param event: event when message is written
    :param vk_api: VK API
    :return: None
    """

    message = detect_intent(event.text)
    if message is not None:
        vk_api.messages.send(
            user_id=event.user_id,
            message=message,
            random_id=random.randint(1,1000),
        )


if __name__ == "__main__":
    logger = logging.getLogger(__file__)
    logging.basicConfig(format="%(process)d %(levelname)s %(message)s")
    logger.setLevel(logging.INFO)

    load_dotenv()
    vk_session = vk_api.VkApi(token=os.getenv("VK_TOKEN"))
    vk_api = vk_session.get_api()

    longpoll = VkLongPoll(vk_session)

    for event in longpoll.listen():
        if event.type == VkEventType.MESSAGE_NEW:
            if event.to_me:
                answer(event, vk_api)
