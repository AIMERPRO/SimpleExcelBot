"""

Created by Oleg Potrebcuk for Work Testing

"""

# imports
import logging
import os

import telebot
import xlsxwriter
from dotenv import load_dotenv
from telebot import types

from db import db_table_add_user, return_users

# Bot Startup
load_dotenv()

TOKEN = str(os.getenv("TOKEN"))

bot = telebot.TeleBot(TOKEN, parse_mode=None)
logger = telebot.logger
telebot.logger.setLevel(logging.DEBUG)

# Startup DataBase
try:
    os.system('alembic upgrade head')
except:
    logger.error('DataBase Already Created')


# Simple /start Handler for Menu
@bot.message_handler(commands=['start'])
def send_welcome(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    markup.add("Добавить работника")

    bot.reply_to(message, "Вы в главном меню", reply_markup=markup)


# Simple text Handler
@bot.message_handler(content_types=['text'])
def new_worker(message):
    if message.text == 'Добавить работника':
        bot.reply_to(message, "Введите ФИО Работника")

        bot.register_next_step_handler_by_chat_id(message.chat.id, add_worker_to_db)  # Next step in State Machine


# Function After FIO Handled
def add_worker_to_db(message):
    db_table_add_user(message.text)  #  ---> Look into db.py file

    users = return_users()  #  ---> Look into db.py file

    # Creating Workbook Xlsx File
    wb = xlsxwriter.Workbook(f'files/{message.from_user.id}.xlsx')
    ws = wb.add_worksheet()

    # Writing rows to the worksheet
    for idx, user in enumerate(users):
        ws.write_row(idx, 0, [user.id, user.fio, user.datar.strftime("%d/%m/%Y"), user.role.name])

    wb.close()

    file = open(f'files/{message.from_user.id}.xlsx', 'rb')

    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    markup.add("Добавить работника")

    # Sending our document and return to the Main Menu
    bot.send_document(message.chat.id, file)

    bot.send_message(message.chat.id, 'Вы в главном меню', reply_markup=markup)

    file.close()


# Start bot
bot.infinity_polling()
