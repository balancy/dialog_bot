import logging
import random
from telegram.bot import Bot

import vk_api
from vk_api.longpoll import VkLongPoll, VkEventType

from config import TG_LOGS_BOT_API_TOKEN, TG_USER_CHAT_ID, VK_TOKEN
from logs_handler import TelegramLogsHandler
from dialogflow_intents.detection import detect_intent


logger = logging.getLogger(__file__)


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
    logs_bot = Bot(token=TG_LOGS_BOT_API_TOKEN)
    logger.addHandler(TelegramLogsHandler(logs_bot, TG_USER_CHAT_ID))
    logger.setLevel("INFO")

    vk_session = vk_api.VkApi(token=VK_TOKEN)
    vk_api = vk_session.get_api()

    longpoll = VkLongPoll(vk_session)

    for event in longpoll.listen():
        if event.type == VkEventType.MESSAGE_NEW:
            if event.to_me:
                answer(event, vk_api)
