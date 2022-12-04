import telebot as tb
from telebot import types as tp
import bot_token
import bot_parameters as pm
import sqlite3
from datetime import datetime

bot = tb.TeleBot(bot_token.tk)
kolvo = []

@bot.message_handler(commands=['start']) #самое начало бота, когда пользователь только активирует его

def send_mes(message): # функция, где есть привественный текст
    kolvo.append(message.from_user.username)
    bot.send_message(message.chat.id, pm.welcome)
    klava(message)

@bot.message_handler(commands=['kolvo']) # команда, чтоб посмотреть челов, которые старт нажали в боте
def uchastniki(message):
    lol = len(set(kolvo))
    bot.send_message(message.chat.id, f'{pm.numbers} {lol}')

def klava(message): # клавиатура, где есть расписание мп и регистрация
    klava = tp.ReplyKeyboardMarkup(resize_keyboard= True, row_width=2)
    answ12 = tp.KeyboardButton(text=pm.registr)
    answ2 = tp.KeyboardButton(text='Расписание мероприятий')
    klava.add(answ2, answ12)
    bot.send_message(message.chat.id, '555', reply_markup=klava)
    bot.send_message(1756196334, message.from_user.username)

    @bot.message_handler(func=lambda message: message.text == 'Расписание мероприятий')
    def time_to_events(message):
        conn = sqlite3.connect('sqlite3.db')
        cur = conn.cursor()

        for i in range(int(cur.execute("SELECT MAX (id) FROM event_list").fetchone()[0])):
            print()


@bot.message_handler(func=lambda message: 'Регистрация' in message.text)
def spisok_registr(message):
    klava = tp.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    answ1 = tp.KeyboardButton(text=pm.mp1)
    answ2 = tp.KeyboardButton(text=pm.mp2)
    answ3 = tp.KeyboardButton(text=pm.mp3)
    beck = tp.KeyboardButton(text=pm.back)
    klava.add(answ1, answ2, answ3, beck)
    bot.send_message(message.chat.id, pm.spisok, reply_markup=klava)

    @bot.message_handler(func=lambda message: message.text == pm.mp1)
    def registr(message):
        if message.text == pm.mp1:
            s = bot.send_message(message.chat.id, pm.dlya_registr)
            bot.register_next_step_handler(s, reg)

    @bot.message_handler(func=lambda message: message.text == pm.mp2)
    def create_event(message):
        if message.text == pm.mp2:
            s = bot.send_message(message.chat.id, pm.to_create)
            bot.register_next_step_handler(s, create)


def reg(message):
    conn = sqlite3.connect('sqlite3.db')
    cur = conn.cursor()

    user_info = []
    user_info.append(message.text.split())

    bot.send_message(message.chat.id, pm.blagodar)

    surname = (user_info[0][0])
    name = (user_info[0][1])
    email = (user_info[0][2])
    add = (surname, name, email)



    users_counter = int(cur.execute("SELECT MAX (id) FROM event").fetchone()[0])

    print(users_counter)

    cur.execute("INSERT INTO event (surname, name, email) VALUES (?, ?, ?);", add)
    conn.commit()

def create(message):
    conn = sqlite3.connect('sqlite3.db')
    cur = conn.cursor()

    event_info = []
    event_info.append(message.text.split())

    bot.send_message(message.chat.id, pm.creating_event_text)

    name_event = (event_info[0][0])
    manager = (event_info[0][1])
    manager_email = (event_info[0][2])
    user_count = 1
    add = (name_event, manager, manager_email, user_count, str(datetime.now().date()))

    cur.execute("INSERT INTO event_list (name_event, manager, manager_email, user_count, date_register) VALUES (?, ?, ?, ?, ?);", add)
    conn.commit()

@bot.message_handler(func=lambda message: pm.back in message.text)
def back(message):
    bot.send_message(message.chat.id, pm.menyu)
    klava(message)


bot.infinity_polling()
