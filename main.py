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
@bot.message_handler(commands=['start'])
def game(message):
    markup = utils.generate_markup_lite()
    bot.send_message(message.chat.id, 'Hello! This is unoficial shuffler-bot for "Welcome to" board game. You need to have original game for using this bot. press button to start game', reply_markup=markup)

@bot.message_handler(commands=['StartGame'])
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
    deck.append(rowtop1[0])
    deck.append(rowtop2[0])
    deck.append(rowtop3[0])
    # Получаем строки из БД
    bot.send_message(message.chat.id, 'Woo-ho, new round!', reply_markup=markup)
    bot.send_media_group(message.chat.id, [types.InputMediaPhoto(rowtop1[1]),types.InputMediaPhoto(rowbot1[2])])
    bot.send_media_group(message.chat.id, [types.InputMediaPhoto(rowtop2[1]),types.InputMediaPhoto(rowbot2[2])])
    bot.send_media_group(message.chat.id, [types.InputMediaPhoto(rowtop3[1]),types.InputMediaPhoto(rowbot3[2])])
    #bot.send_media_group(message.chat.id, [{'type': 'photo', 'media': rowtop3[1]}, {'type': 'photo', 'media': rowbot3[2]}])
    utils.set_user_game(message.chat.id, deck)

    # Отсоединяемся от БД
    db_worker.close()

@bot.message_handler(commands=['shuflle'])
def shuflle(message):
    # Подключаемся к БД
    db_worker = SQLighter(config.database_name)
    # Формируем разметку
    markup = utils.generate_markup()
    # Отправляем аудиофайл с вариантами ответа
    # bot.send_photo(message.chat.id, row[1], reply_markup=markup)
    # Включаем "игровой режим"
    deck = []
    for i in range(81):
        deck.append(i + 1)
    random.shuffle(deck)

    rowbot1 = db_worker.select_single(deck.pop())
    rowbot2 = db_worker.select_single(deck.pop())
    rowbot3 = db_worker.select_single(deck.pop())
    rowtop1 = db_worker.select_single(deck.pop())
    rowtop2 = db_worker.select_single(deck.pop())
    rowtop3 = db_worker.select_single(deck.pop())
    deck.append(rowtop1[0])
    deck.append(rowtop2[0])
    deck.append(rowtop3[0])
    # Получаем строки из БД
    bot.send_message(message.chat.id, 'Woo-ho, shuffle!', reply_markup=markup)
    bot.send_media_group(message.chat.id, [types.InputMediaPhoto(rowtop1[1]), types.InputMediaPhoto(rowbot1[2])])
    bot.send_media_group(message.chat.id, [types.InputMediaPhoto(rowtop2[1]), types.InputMediaPhoto(rowbot2[2])])
    bot.send_media_group(message.chat.id, [types.InputMediaPhoto(rowtop3[1]), types.InputMediaPhoto(rowbot3[2])])

    utils.set_user_game(message.chat.id, deck)

    db_worker.close()


@bot.message_handler(commands=['next'])
def next(message):
    # Подключаемся к БД
    db_worker = SQLighter(config.database_name)
    # Формируем разметку
    markup = utils.generate_markup()
    # Отправляем аудиофайл с вариантами ответа
    # bot.send_photo(message.chat.id, row[1], reply_markup=markup)
    # Включаем "игровой режим"
    deck = utils.get_deck_for_user(message.chat.id)
    if (len(deck)<6):
        if (len(deck)>2):
            rowbot1 = db_worker.select_single(deck.pop())
            rowbot2 = db_worker.select_single(deck.pop())
            rowbot3 = db_worker.select_single(deck.pop())
        deck = []
        for i in range(81):
            deck.append(i + 1)
        random.shuffle(deck)
        if (len(deck) > 2):
            deck.append(rowbot1[0])
            deck.append(rowbot2[0])
            deck.append(rowbot3[0])
    rowbot1 = db_worker.select_single(deck.pop())
    rowbot2 = db_worker.select_single(deck.pop())
    rowbot3 = db_worker.select_single(deck.pop())
    rowtop1 = db_worker.select_single(deck.pop())
    rowtop2 = db_worker.select_single(deck.pop())
    rowtop3 = db_worker.select_single(deck.pop())
    deck.append(rowtop1[0])
    deck.append(rowtop2[0])
    deck.append(rowtop3[0])
    # Получаем строки из БД
    bot.send_message(message.chat.id, 'Woo-ho, new round!', reply_markup=markup)
    bot.send_media_group(message.chat.id, [types.InputMediaPhoto(rowtop1[1]), types.InputMediaPhoto(rowbot1[2])])
    bot.send_media_group(message.chat.id, [types.InputMediaPhoto(rowtop2[1]), types.InputMediaPhoto(rowbot2[2])])
    bot.send_media_group(message.chat.id, [types.InputMediaPhoto(rowtop3[1]), types.InputMediaPhoto(rowbot3[2])])

    utils.set_user_game(message.chat.id, deck)

    # Отсоединяемся от БД
    db_worker.close()
@bot.message_handler(commands=['end'])
def end(message):
    utils.finish_user_game(message.chat.id)
    markup = utils.generate_markup_lite()
    bot.send_message(message.chat.id, 'Thank you for playing!', reply_markup=markup)


@bot.message_handler(func=lambda message: True, content_types=['text'])
def check_answer(message):
    # Если функция возвращает None -> Человек не в игре
    if (utils.get_deck_for_user(message.chat.id)):
        markup = utils.generate_markup()
    else:
        markup = utils.generate_markup_lite()
    bot.send_message(message.chat.id,'Oh,no, just choose the button.',reply_markup=markup)


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
