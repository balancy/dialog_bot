import os
import random

from dotenv import load_dotenv
import vk_api
from vk_api.longpoll import VkLongPoll, VkEventType

from intent_handlers import detect_intent


def answer(event, vk_api):
    vk_api.messages.send(
        user_id=event.user_id,
        message=detect_intent(event.text),
        random_id=random.randint(1,1000),
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
