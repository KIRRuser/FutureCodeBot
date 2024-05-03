# # # Модули бота

import qrcode
import wikipedia

import newTEST

wikipedia.set_lang('ru')
import random
import sqlite3
import requests
import json
from datetime import *
from langdetect import detect
import pymorphy2
from amzqr import amzqr

# # # Слова для вас, любимые*

s1 =['Привет','Салют','Хай','Приветствую','Йоу','Шалом','Хаю-хай','Бонжур','Здароу',]
s2 = ['Йоу','Бип','Бап','Тук','Рад тебя видеть','Мерси','Лавки','143']

# # # Создание таблицы SQlite3

conn = sqlite3.connect('userdata.db')
c = conn.cursor()

c.execute('''CREATE TABLE IF NOT EXISTS users
             (id INTEGER PRIMARY KEY, username TEXT, first_name TEXT, last_name TEXT, date TEXT, time TEXT, city TEXT, url TEXT, wikirequest TEXT)''')

conn.commit()
conn.close()


# # # Бот

import telebot
from telebot import types
import config_tgbot


class Buttons:
    def __init__(self):
        self.btn_main = types.InlineKeyboardButton(text="Меню", callback_data='main')


class Bot:
    def __init__(self,token):
        self.bot = telebot.TeleBot(token)
        self.weather_api = config_tgbot.weather_token


# # # Начало работы бота

    def start(self):

        # # # Обработчик команды /start

        @self.bot.message_handler(commands=['start'])
        def command_start(message):
            hello = random.choice(s1)
            keyboard = types.InlineKeyboardMarkup(row_width=1)
            btn_start = types.InlineKeyboardButton(text="тык", callback_data="help")
            keyboard.add(btn_start)
            self.bot.send_message(message.chat.id, hello + f", {message.from_user.first_name}!",
                             reply_markup=keyboard)



            chat_id = message.chat.id
            user_first_name = message.from_user.first_name
            user_last_name = message.from_user.last_name
            username = message.from_user.username

            now = datetime.now()
            current_time = now.strftime("%H:%M:%S")

            current_date = date.today()


            connect = sqlite3.connect('userdata.db')
            cursor = connect.cursor()
            cursor.execute(f'SELECT id FROM users WHERE id = {chat_id}')
            data = cursor.fetchone()

            if data is None:
                cursor.execute('''INSERT INTO users (id, username, first_name, last_name, date, time)
                            VALUES (?, ?, ?, ?, ?, ?)''', (chat_id, username, user_first_name, user_last_name, current_date, current_time))
                connect.commit()
            else:
                pass

        # # # Обработчик Callback.data

        @self.bot.callback_query_handler(func=lambda callback: callback.data)
        def check_cb(callback):
            if callback.data == 'help':
                well = random.choice(s2)
                keyboard = types.InlineKeyboardMarkup()
                btn_we = types.InlineKeyboardButton(text='Посмотреть погоду',
                                                    callback_data='weather')
                keyboard.row(btn_we)
                btn_qr = types.InlineKeyboardButton(text='Создать QR код',
                                                    callback_data='qrcode')
                btn_wi = types.InlineKeyboardButton(text='Искать в Википедии',
                                                   callback_data='wiki')
                keyboard.add(btn_qr, btn_wi)
                self.bot.edit_message_text(chat_id=callback.message.chat.id,
                                    message_id=callback.message.id,
                                    text=f'{well}, {callback.from_user.first_name},'
                                    ' я могу:',
                                    reply_markup=keyboard)


            if callback.data == 'weather':
                self.bot.edit_message_text(chat_id=callback.message.chat.id,
                                      message_id=callback.message.id,
                                      text=f'{callback.from_user.first_name}, введи свой город!',
                                      reply_markup=None)
                self.bot.register_next_step_handler(callback.message, get_weather)


            if callback.data == 'main':
                well = random.choice(s2)
                keyboard = types.InlineKeyboardMarkup()
                btn_we = types.InlineKeyboardButton(text='Посмотреть погоду',
                                                    callback_data='weather')
                keyboard.row(btn_we)
                btn_qr = types.InlineKeyboardButton(text='Создать QR код',
                                                    callback_data='qrcode')
                btn_s = types.InlineKeyboardButton(text='Искать в Википедии',
                                                   callback_data='wiki')
                keyboard.add(btn_qr, btn_s)
                self.bot.edit_message_text(chat_id=callback.message.chat.id,
                                      message_id=callback.message.id,
                                      text=f'{well}, {callback.from_user.first_name}!',
                                      reply_markup=keyboard)



            if callback.data == 'qrcode':
                keyboard = types.InlineKeyboardMarkup(row_width=2)
                btn_yes = types.InlineKeyboardButton(text='Добавить фото',
                                                     callback_data='yes')
                btn_no = types.InlineKeyboardButton(text='Продолжить без фото',
                                                    callback_data='no')
                keyboard.add(btn_yes,btn_no)
                self.bot.edit_message_text(chat_id=callback.message.chat.id,
                                      message_id=callback.message.id,
                                      text=f'{callback.from_user.first_name}, я могу добавить фотографию к твоему QR коду!',
                                      reply_markup=keyboard)
            if callback.data == 'yes':
                self.bot.edit_message_text(chat_id=callback.message.chat.id,
                                           message_id=callback.message.id,
                                           text=f'{callback.from_user.first_name}, пришли фото',
                                           reply_markup=None)
                self.bot.register_next_step_handler(callback.message, get_photo)


            if callback.data == 'no':
                ph = None
                self.bot.edit_message_text(chat_id=callback.message.chat.id,
                                           message_id=callback.message.id,
                                           text=f'{callback.from_user.first_name}, введи ссылку',
                                           reply_markup=None)
                self.bot.register_next_step_handler(callback.message, qrcode_creation_without_photo)

            if callback.data == 'reply':
                self.bot.edit_message_text(chat_id=callback.message.chat.id,
                                           message_id=callback.message.id,
                                           text=f'{callback.from_user.first_name}, введи размер',
                                           reply_markup=None)
                self.bot.register_next_step_handler(callback.message, get_size)


            if callback.data == 'wiki':
                self.bot.edit_message_text(chat_id=callback.message.chat.id,
                                      message_id=callback.message.id,
                                      text=f'{callback.from_user.first_name}, введи запрос',
                                      reply_markup=None)
                self.bot.register_next_step_handler(callback.message, wiki_copy)

        # # # Погода

        def get_weather(message):
            try:
                citysqlite = message.text.title()
                connect = sqlite3.connect('userdata.db')
                cursor = connect.cursor()
                cursor.execute("UPDATE users SET city = ? WHERE id = ?",
                               (citysqlite, message.chat.id))
                connect.commit()
                connect.close()
                now = datetime.now()
                current_time = now.strftime("%H:%M:%S")
                keyboard = types.InlineKeyboardMarkup(row_width=1)
                btn_new = types.InlineKeyboardButton(text='Изменить город', callback_data='weather')
                btn_main = types.InlineKeyboardButton(text='Меню', callback_data='main')
                keyboard.add(btn_new, btn_main)
                city = message.text.strip().title()
                weather = requests.get(
                    f'https://api.openweathermap.org/data/2.5/weather?q={city}&appid={self.weather_api}&units=metric')
                data = json.loads(weather.text)
                import deg
                deg = deg.direction(data["wind"]["deg"])
                if detect(city) == 'ru' or city[-1] == 'ь':
                    morph = pymorphy2.MorphAnalyzer()
                    citye = morph.parse(city)[0]
                    cityew = citye.inflect({'loct'}).word.title()
                    self.bot.send_message(chat_id=message.from_user.id,
                                     text=
                                     f'Сейчас в {cityew} {data["main"]["temp"]}°\n'
                                     f'Макс.: {data["main"]["temp_max"]}°, мин.: {data["main"]["temp_min"]}°\n'
                                     f'Ветер: {data["wind"]["speed"]} м/с, направление: {deg} \n\n'
                                     f'Данные на момент времени {current_time}',
                                     reply_markup=None)
                else:
                    self.bot.send_message(chat_id=message.from_user.id,
                                          text=
                                          f'Сейчас в {city} {data["main"]["temp"]}°\n'
                                          f'Макс.: {data["main"]["temp_max"]}°, мин.: {data["main"]["temp_min"]}°\n'
                                          f'Ветер: {data["wind"]["speed"]} м/с, направление: {deg}\n\n'
                                          f'Данные на момент времени {current_time}',
                                          reply_markup=None)
            except:
                self.bot.send_message(chat_id=message.from_user.id,
                                 text='Ошибка запроса #401')
            self.bot.send_message(chat_id=message.from_user.id,
                             text=f'Каков план, {message.from_user.first_name}?',
                             reply_markup=keyboard)

        # # # Википедия

        def wiki_copy(message):
            wikirequest = message.text
            connect = sqlite3.connect('userdata.db')
            cursor = connect.cursor()
            cursor.execute("UPDATE users SET wikirequest = ? WHERE id = ?",
                           (wikirequest, message.chat.id))
            connect.commit()
            connect.close()
            keyboard = types.InlineKeyboardMarkup(row_width=2)
            btn_repeat = types.InlineKeyboardButton(text="Еще запрос", callback_data='wiki')
            btn_main = types.InlineKeyboardButton(text="Меню", callback_data='main')
            keyboard.add(btn_repeat, btn_main)
            try:
                self.bot.send_message(chat_id=message.from_user.id,
                                        text=wikipedia.summary(message.text))
            except:
                self.bot.send_message(chat_id=message.from_user.id,
                                        text='Ошибка запроса #400')
            self.bot.send_message(chat_id=message.from_user.id,
                            text=f'{message.from_user.first_name}, Каков план?',
                            reply_markup=keyboard)

        # # # QR code с фото
        def get_photo(message):
            photo = message.photo[-1]
            file_info = self.bot.get_file(photo.file_id)
            downloaded_file = self.bot.download_file(file_info.file_path)
            save_path = 'user_photo_for_qr.jpg'
            with open(save_path, 'wb') as new_file:
                new_file.write(downloaded_file)
            self.bot.send_message(message.chat.id, f'{message.from_user.first_name}, введи размер QR кода (10-20)')
            self.bot.register_next_step_handler(message, get_size)

        def get_size(message):
            try:
                global size
                size = int(message.text)
                if size < 10:
                    size = 10
                if size > 20:
                    size = 20
                self.bot.send_message(message.chat.id,'введи ссылку')
                self.bot.register_next_step_handler(message, qrcode_creation_with_photo)
            except:
                keyboard = types.InlineKeyboardMarkup(row_width=1)
                btn_reply = types.InlineKeyboardButton(text='Повторить',
                                                       callback_data='reply')
                btn_main = types.InlineKeyboardButton(text='Меню',
                                                      callback_data='main')
                keyboard.add(btn_reply,btn_main)
                self.bot.send_message(message.chat.id, 'Некорректный ввод!',
                                      reply_markup=keyboard)


        def qrcode_creation_with_photo(message):
            url = message.text
            connect = sqlite3.connect('userdata.db')
            cursor = connect.cursor()
            cursor.execute("UPDATE users SET url = ? WHERE id = ?",
                           (url, message.chat.id))
            connect.commit()
            connect.close()
            try:
                qrcode = amzqr.run(
                    words=url,
                    version=size,
                    level='H',
                    picture='user_photo_for_qr.jpg',
                    colorized=True
                )
                user_qr = open('user_photo_for_qr_qrcode.png', 'rb')
                self.bot.send_photo(message.chat.id, user_qr)
                user_qr.close()

                keyboard = types.InlineKeyboardMarkup(row_width=2)
                btn_repeat = types.InlineKeyboardButton(text="Создать еще", callback_data='qrcode')
                btn_main = types.InlineKeyboardButton(text="Меню", callback_data='main')
                keyboard.add(btn_repeat,btn_main)
                self.bot.send_message(message.chat.id,f'{message.from_user.first_name}, каков план?',
                                      reply_markup=keyboard)
            except:
                keyboard = types.InlineKeyboardMarkup(row_width=1)
                btn_main = types.InlineKeyboardButton(text="Меню", callback_data='main')
                keyboard.add(btn_main)
                self.bot.send_message(message.chat.id, 'Неизвестная ошибка! сообщи об этом @cleontheseventeenth',
                                      reply_markup=keyboard)

        # # # QR code без фото
        def qrcode_creation_without_photo(message):
            url = message.text
            connect = sqlite3.connect('userdata.db')
            cursor = connect.cursor()
            cursor.execute("UPDATE users SET url = ? WHERE id = ?",
                           (url, message.chat.id))
            connect.commit()
            connect.close()
            try:
                qrcode = amzqr.run(words=url)
                user_qr = open('qrcode.png', 'rb')
                self.bot.send_photo(message.chat.id, user_qr)
                user_qr.close()
                keyboard = types.InlineKeyboardMarkup(row_width=2)
                btn_repeat = types.InlineKeyboardButton(text="Создать еще", callback_data='qrcode')
                btn_main = types.InlineKeyboardButton(text="Меню", callback_data='main')
                keyboard.add(btn_repeat, btn_main)
                self.bot.send_message(message.chat.id, f'{message.from_user.first_name}, каков план?',
                                      reply_markup=keyboard)
            except:
                keyboard = types.InlineKeyboardMarkup(row_width=1)
                btn_reply = types.InlineKeyboardButton(text='Повторить',
                                                       callback_data='reply')
                btn_main = types.InlineKeyboardButton(text='Меню',
                                                      callback_data='main')
                keyboard.add(btn_reply, btn_main)
                self.bot.send_message(message.chat.id, 'Некорректный ввод!',
                                      reply_markup=keyboard)

        # # # Ответ бота на голосовые сообщения, видео, файлы, фото...

        @self.bot.message_handler(content_types=['voice'])
        def voice_answer(message):
            answerboard = types.InlineKeyboardMarkup(row_width=1)
            btnanswer = types.InlineKeyboardButton(text="Меню", callback_data='main')
            answerboard.add(btnanswer)
            self.bot.send_message(chat_id=message.from_user.id,
                                  text=f'{message.from_user.first_name},'
                                        f' мне жаль, но я не услышу твой замечательный голос(',
                                        reply_markup=answerboard)

        @self.bot.message_handler(content_types=['video'])
        def voice_answer(message):
            answerboard = types.InlineKeyboardMarkup(row_width=1)
            btnanswer = types.InlineKeyboardButton(text="Меню", callback_data='main')
            answerboard.add(btnanswer)
            self.bot.send_message(chat_id=message.from_user.id,
                                  text=f'{message.from_user.first_name},'
                                        f' мне жаль, но я не посмеюсь с твоего видео((',
                                        reply_markup=answerboard)

        @self.bot.message_handler(content_types=['document'])
        def voice_answer(message):
            answerboard = types.InlineKeyboardMarkup(row_width=1)
            btnanswer = types.InlineKeyboardButton(text="Меню", callback_data='main')
            answerboard.add(btnanswer)
            self.bot.send_message(chat_id=message.from_user.id,
                                  text=f'{message.from_user.first_name},'
                                        f' мне жаль, но я не сделаю за тебя домашку((',
                                        reply_markup=answerboard)
        @self.bot.message_handler(content_types=['sticker'])
        def voice_answer(message):
            answerboard = types.InlineKeyboardMarkup(row_width=1)
            btnanswer = types.InlineKeyboardButton(text="Меню", callback_data='main')
            answerboard.add(btnanswer)
            (self.bot.send_message(chat_id=message.from_user.id,
                                  text=f'{message.from_user.first_name},'
                                        f' это стикер? или меня глючит?',
                                        reply_markup=answerboard))
        @self.bot.message_handler(content_types=['photo'])
        def photo_answer(message):
            answerboard = types.InlineKeyboardMarkup(row_width=1)
            btnanswer = types.InlineKeyboardButton(text="Меню", callback_data='main')
            answerboard.add(btnanswer)
            self.bot.send_message(chat_id=message.from_user.id,
                                  text=f'{message.from_user.first_name},'
                                        f' это точно ты на фотографии?',
                                        reply_markup=answerboard)


        self.bot.polling(none_stop=True)


# # # Запуск бота

if __name__ == "__main__":
    # try:
    token = config_tgbot.bot_token
    bot = Bot(token)
    bot.start()

