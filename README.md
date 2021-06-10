# Speech recognition bot

![App gif](https://s6.gifyu.com/images/bot_small.gif)

Телеграм-бот и бот в группе ВК, которые отвечают на сообщения пользователя с помощью dialogflow API.
Приложение использует библиотеку [Dialogflow](https://dialogflow.cloud.google.com/) от google. Библиотека
позволяет обучить бота естественному языку в определенных лимитах.

Ссылка на бота в Телеграм: [Бот](https://t.me/dvmn_speech_recognition_bot)

Ссылка на бота в Вк: [Сообщения группы](https://vk.com/im?media=&sel=-203801849)

Бот отвечает на те фразы, которые знает. Если он не понимает, что ему пишут, он промолчит, чтобы 
администраторы канала могли ответить.

## Install

Python3 and Git should be already installed. 

1. Clone the repository by command:
```console
git clone https://github.com/balancy/speech_recognition_bot
```

2. Go inside cloned repository and create virtual environment by command:
```console
python -m venv env
```

3. Activate virtual environment. For linux-based OS:
```console
source env/bin/activate
```
&nbsp;&nbsp;&nbsp;
For Windows:
```console
env\scripts\activate
```

4. Install requirements by command:
```console
pip install -r requirements.txt
```

5. Rename `.env.example` to `.env` and define your propre values for environmental variables:

- `TG_BOT_API_TOKEN` - token of your telegram bot
- `TG_BOT_CHAT_ID` - your chat id in telegram
- `DIALOG_FLOW_PROJECT_ID` - id of your dialogflow project
- `DIALOG_FLOW_SESSION_ID` - id of your dialogflow session
- `GOOGLE_APPLICATION_CREDENTIALS` - json file-key with your google credentials 
- `VK_TOKEN` - token of your vkontakte group

## Launch

1. Run telegram bot
```console
python3 telegram_bot.py
```

2. Run vkontakte bot
```console
python3 vk_long_polling.py
```