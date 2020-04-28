import config
import functions as f               # terrible alias
import strings
import keyboard as kb
import inlineRealization as iRz
import workWithDataBase as wDB

import telebot
from telebot import types
from telebot.types import Message

# TOKEN = os.environ.get('TELEGRAM_BOT_FOR_VEGA_TOKEN')
TOKEN = config.token

bot = telebot.TeleBot(TOKEN)

wDB.init_data_base()


@bot.message_handler(commands=['start'])
def process_start_command(message: Message):
    bot.send_message(message.from_user.id,
                     '\n'.join([f'Привет, {message.from_user.username}!',
                                'Выберите:']),
                     reply_markup=kb.choiceMarkup)
    wDB.add_user(chat_id=message.chat.id)

    # add to event-log
    # print('+ in bot: ' + str(message.chat.id) + ' ' + str(message.from_user.username))
    # print('+ in bot: ' + '/start')


@bot.message_handler(commands=['setnew'])
def time_table_changed(message: Message):
    if f.isAdmin(message.chat.id):
        str = message.text.split(' ')
        option = ''
        if len(str) > 1:
            for i in range(1, len(str)):
                option += str[i] + ' '
        f.sendNotif(option)
        print('+ in bot: ' + str(message.chat.id))
        print('+ in bot: ' + '/setnew ' + option)
    else:
        # add to log
        # use format-strings
        print("----- ВНИМАНИЕ!!! \n----- пользователь, НЕ ЯВЛЯЮЩИЙСЯ АДМИНОМ использовал"
              "'setnew'\n----- chat_id: " + str(message.chat.id)
              + "\n----- username: " + str(message.from_user.username))


@bot.message_handler(commands=['help'])
def send_list_of_commands(message: Message):
    bot.send_message(message.chat.id, strings.INSTROUCTIONS_HELP)
    print('+ in bot: ' + str(message.chat.id) + ' - ' + str(message.from_user.username))
    print('+ in bot: ' + '/help')


@bot.message_handler(content_types=['text'])
def repeat_message(message: Message):
    wDB.add_user(chat_id=message.chat.id)
    f.general_func(message)
    print('+ in bot: ' + str(message.chat.id) + ' - ' + str(message.from_user.username))
    print('+ in bot: ' + '/text')
    print('+ in bot: ' + "'" + message.text + "'")


@bot.inline_handler(func=lambda query: len(query.query) > 0)
def query_text(query):
    print('query: ' + query.query)
    strOut = iRz.general_func(query)
    bot.answer_inline_query(query.id, strOut)


if __name__ == '__main__':
    bot.polling(none_stop=True)
