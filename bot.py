# script version 1.1
import telebot
from google_sheets.create_doc import create_doc
from credentials.config import settings
from flask import Flask, request

dates_and_employer_name = []
white_list = [
    settings.USER_1,
    settings.USER_2,
    settings.USER_3,
    settings.USER_4,
    settings.USER_5,
]

bot = telebot.TeleBot(settings.TOKEN, threaded=False)
webhook_url = settings.WEBHOOK_URL
bot.remove_webhook()
bot.set_webhook(webhook_url)

app = Flask(__name__)


@app.route('/', methods=['POST'])
def webhook():
    update = telebot.types.Update.de_json(request.stream.read().decode('utf-8'))
    bot.process_new_updates([update])
    return 'ok', 200


def new_start_message(message_chat_id):
    """Template answer to user after /start command and finish result"""
    bot.send_message(
        message_chat_id, "Чтобы начать работу введите /create или /help для справки"
    )


def create_result(first_date, second_date, employer_name):
    """Function for start creating user's document and give him URL of this doc"""
    url = create_doc(first_date, second_date, employer_name)
    return url


@bot.message_handler(commands=["check"])
def check_permission(message):
    """Check is there user in white list"""
    if message.chat.username in white_list:
        bot.reply_to(message, "Вы в белом списке")
    else:
        bot.reply_to(message, "Вы не в белом списке")


@bot.message_handler(commands=["start"])
def start(message):
    """Start command for using bot"""
    new_start_message(message.chat.id)


@bot.message_handler(commands=["create"])
def create(message):
    """Command for start create_doc script"""
    if message.chat.username in white_list:
        dates_and_employer_name.clear()
        msg = bot.reply_to(
            message, "Введена команда /create. Введите первую дату например 01.01.21"
        )
        bot.register_next_step_handler(msg, get_a_first_date)
    else:
        bot.reply_to(message, "Вы не в белом списке")
        new_start_message(message.chat.id)


def get_a_first_date(message):
    """Get first date from user"""
    if message.content_type == "text":
        dates_and_employer_name.append(message.text)
        bot.register_next_step_handler(message, get_a_second_date)
        bot.send_message(message.chat.id, text="Введите вторую дату")
    else:
        bot.send_message(
            message.chat.id, text="Нужно ввести дату, начните сначала..."
        )
        new_start_message(message.chat.id)


def get_a_second_date(message):
    """Get second date from user"""
    if message.content_type == "text":
        dates_and_employer_name.append(message.text)
        bot.register_next_step_handler(message, get_a_employer_name)
        bot.send_message(message.chat.id, text="Введите свою фамилию и инициалы")


def get_a_employer_name(message):
    """Get name from user"""
    if message.content_type == "text":
        dates_and_employer_name.append(message.text)
        markup = telebot.types.InlineKeyboardMarkup()
        markup.add(
            telebot.types.InlineKeyboardButton(
                text="Сделать отчет", callback_data="create_result"
            )
        )
        markup.add(
            telebot.types.InlineKeyboardButton(
                text="Отменить", callback_data="cancel"
            )
        )

        bot.send_message(
            message.chat.id,
            text="Принято две даты...Нажмите 'Сделать отчет' для подтверждения или 'Отменить' для отмены",
            reply_markup=markup,
        )


@bot.callback_query_handler(func=lambda call: True)
def make_decision(call):
    if call.data == "create_result":
        bot.send_message(call.message.chat.id, text="Подождите, делаю отчет...")
        try:
            result = create_result(dates_and_employer_name[0], dates_and_employer_name[1],
                                   dates_and_employer_name[2])
            if result is None:
                bot.send_message(
                    call.message.chat.id,
                    text="Таких дат не существует, проверьте таблицу ",
                )
                new_start_message(call.message.chat.id)
            else:
                bot.send_message(
                    call.message.chat.id, text="Ваш отчет доступен по ссылке:"
                )
                bot.send_message(call.message.chat.id, text=result)
                new_start_message(call.message.chat.id)
        except Exception as e:
            bot.send_message(
                call.message.chat.id, text=str(e)
            )

            bot.send_message(
                call.message.chat.id, text="Что-то пошло не так пишите креведкину"
            )
            new_start_message(call.message.chat.id)
    elif call.data == "cancel":
        bot.send_message(call.message.chat.id, text="Отменено пользователем")
        new_start_message(call.message.chat.id)
    else:
        bot.send_message(
            call.message.chat.id, text="Ничего не понял, давай по новой..."
        )
        new_start_message(call.message.chat.id)


@bot.message_handler(commands=["help"])
def help(message):
    bot.reply_to(
        message,
        "Для начала работы с ботом введите команду /create."
        "Бот запросит у вас дату, введите первую дату командировки "
        "например 01.02.20 далее он запросит вторую дату введите вторую дату командировки "
        "нажмите кнопку 'сделать отчет', после чего бот пришлет ссылку на готовый документ."
        "Пройдите по ней, и нажмите 'скачать как документ Excel'",
    )
