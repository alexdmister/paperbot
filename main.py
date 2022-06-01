# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
import os
import telebot
import time
import random
import config
import utils
import SQLighter
from SQLighter import SQLighter
from telebot import types
bot = telebot.TeleBot(config.token)
currentfront1 = 0
currentfront2 = 0
currentfront3 = 0
@bot.message_handler(commands=['start'])
def game(message):
    # Подключаемся к БД
    db_worker = SQLighter(config.database_name)
    # Формируем разметку
    markup = utils.generate_markup()
    # Отправляем аудиофайл с вариантами ответа
    #bot.send_photo(message.chat.id, row[1], reply_markup=markup)
    # Включаем "игровой режим"
    deck=[]
    for i in range(81):
        deck.append(i+1)
    random.shuffle(deck)

    rowbot1 = db_worker.select_single(deck.pop())
    rowbot2 = db_worker.select_single(deck.pop())
    rowbot3 = db_worker.select_single(deck.pop())
    rowtop1 = db_worker.select_single(deck.pop())
    rowtop2 = db_worker.select_single(deck.pop())
    rowtop3 = db_worker.select_single(deck.pop())
    deck.append(rowtop1)
    deck.append(rowtop2)
    deck.append(rowtop3)
    # Получаем строки из БД
    bot.send_media_group(message.chat.id, [types.InputMediaPhoto(rowtop1[1]),types.InputMediaPhoto(rowbot1[2])])
    bot.send_media_group(message.chat.id, [types.InputMediaPhoto(rowtop2[1]),types.InputMediaPhoto(rowbot2[2])])
    bot.send_media_group(message.chat.id, [types.InputMediaPhoto(rowtop3[1]),types.InputMediaPhoto(rowbot3[2])])
    #bot.send_media_group(message.chat.id, [{'type': 'photo', 'media': rowtop3[1]}, {'type': 'photo', 'media': rowbot3[2]}])
    utils.set_user_game(message.chat.id, deck)
    bot.send_message(message.chat.id, 's', reply_markup=markup)
    # Отсоединяемся от БД
    db_worker.close()

@bot.message_handler(commands=['shuflle'])
def game(message):
    # Подключаемся к БД
    db_worker = SQLighter(config.database_name)
    # Получаем случайную строку из БД
    row = db_worker.select_single(random.randint(1, utils.get_rows_count()))
    # Формируем разметку
    markup = utils.generate_markup(row[2], row[3])
    # Отправляем аудиофайл с вариантами ответа
    bot.send_voice(message.chat.id, row[1], reply_markup=markup)
    # Включаем "игровой режим"
    utils.set_user_game(message.chat.id, row[2])
    # Отсоединяемся от БД
    db_worker.close()
@bot.message_handler(commands=['next'])
def game(message):
    # Подключаемся к БД
    db_worker = SQLighter(config.database_name)
    # Получаем случайную строку из БД
    row = db_worker.select_single(random.randint(1, utils.get_rows_count()))
    # Формируем разметку
    markup = utils.generate_markup(row[2], row[3])
    # Отправляем аудиофайл с вариантами ответа
    bot.send_voice(message.chat.id, row[1], reply_markup=markup)
    # Включаем "игровой режим"
    utils.set_user_game(message.chat.id, row[2])
    # Отсоединяемся от БД
    db_worker.close()
@bot.message_handler(commands=['end'])
def game(message):
    # Подключаемся к БД
    db_worker = SQLighter(config.database_name)
    # Получаем случайную строку из БД
    row = db_worker.select_single(random.randint(1, utils.get_rows_count()))
    # Формируем разметку
    markup = utils.generate_markup(row[2], row[3])
    # Отправляем аудиофайл с вариантами ответа
    bot.send_voice(message.chat.id, row[1], reply_markup=markup)
    # Включаем "игровой режим"
    utils.set_user_game(message.chat.id, row[2])
    # Отсоединяемся от БД
    db_worker.close()
    
@bot.message_handler(func=lambda message: True, content_types=['text'])
def check_answer(message):
    # Если функция возвращает None -> Человек не в игре
    answer = utils.get_answer_for_user(message.chat.id)
    # Как Вы помните, answer может быть либо текст, либо None
    # Если None:
    if not answer:
        bot.send_message(message.chat.id, 'Чтобы начать игру, выберите команду /game')
    else:
        # Уберем клавиатуру с вариантами ответа.
        keyboard_hider = types.ReplyKeyboardRemove()
        # Если ответ правильный/неправильный
        if message.text == answer:
            bot.send_message(message.chat.id, 'Верно!', reply_markup=keyboard_hider)
        else:
            bot.send_message(message.chat.id, 'Увы, Вы не угадали. Попробуйте ещё раз!', reply_markup=keyboard_hider)
        # Удаляем юзера из хранилища (игра закончена)
        utils.finish_user_game(message.chat.id)

'''
@bot.message_handler(commands=['test'])
def find_file_ids(message):
    for file in os.listdir('cards/'):
        if file.split('.')[-1] == 'png':
            f = open('cards/'+file, 'rb')
            msg = bot.send_photo (message.chat.id, f, None)
            # А теперь отправим вслед за файлом его file_id
            print(msg)
        time.sleep(3)
'''

if __name__ == '__main__':
    utils.count_rows()
    random.seed()
    bot.infinity_polling()
# See PyCharm help at https://www.jetbrains.com/help/pycharm/
