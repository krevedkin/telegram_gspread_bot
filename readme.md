# telegram_gspread_bot

![Alt text](img/demo.gif)

#About

Telegram bot for work with google spreadsheets. This telegram bot works with **telebot** and **gspread** packages.  
Developed by using **Python3.9** (but also works with **Python 3.8** version).
You have to install requirements from requirements.txt for using this app 
 

`pip install -r requirements.txt`


It's necessary to use with a file "credentials.json" from googleAPI.
Here's a link with quick guide how to do this.  
https://gspread.readthedocs.io/en/latest/oauth2.html#enable-api-access

Another requirement is use telegram API token from @BotFather.
Here's more information:
https://core.telegram.org/bots/faq#how-do-i-create-a-bot

A file config.py uses **Pydantic Settings** for work with spreadsheets URLs, telegram Token and nicknames of users which have access to bot. All this data is
kept in environment variables or .env file. 

It uses webhooks for handle users requests so I used **Flask** for handle POST requests.

#How it works

The main file is bot.py. This script activates bot and it's waiting for user requests.
After /start command user have to send two dates and his name to bot and push the button for get result.

Script create_doc.py gets these arguments from bot.py and creates a finished document,
after that it returns URL to user in Telegram with a finished doc.
