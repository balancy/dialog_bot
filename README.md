# Dialog bots

![App gif](https://s6.gifyu.com/images/bot_small.gif)

Telegram and Vkontakte bots that could keep simple conversation with the user.
They are based on google [Dialogflow](https://dialogflow.cloud.google.com/) library.
Dialogflow library could teach bot to understand natural language sentences and to respond accordingly.

Link to telegram bot: [Bot](https://t.me/dvmn_speech_recognition_bot)

Link to VK bot: [Messages](https://vk.com/im?media=&sel=-203801849)

Bots could respond to phrases they already know.
If they don't understand what is written, they'll be silent or they'll respond that they couldn't understand.

## Install

At least Python 3.8, as well as Poetry and Git, should be already installed.

1. Clone the repository by command:
```console
git clone git@github.com:balancy/speech_recognition_bot.git
```

2. Go inside cloned repository and activate virtal environment:
```console
poetry shell
```

3. Install dependecies:
```console
poetry install
```

4. Rename `.env.example` to `.env` and define your proper values for environment variables:

- `TG_DIALOG_BOT_API_TOKEN` - token of your dialog telegram bot
- `TG_LOGS_BOT_API_TOKEN` - token of your logs telegram bot
- `TG_USER_CHAT_ID` - your chat id in telegram
- `DIALOG_FLOW_PROJECT_ID` - id of your dialogflow project
- `DIALOG_FLOW_SESSION_ID` - id of your dialogflow session
- `GOOGLE_APPLICATION_CREDENTIALS` - json file-key with your google credentials
- `VK_TOKEN` - token of your vkontakte group

## Launch

1. Run telegram bot
```console
python tg_bot.py
```

2. Run vkontakte bot
```console
python vk_bot.py
```