import telebot
from telebot import types
import sqlite3


bot = telebot.TeleBot('7051141307:AAHLYtGeFpBTUdAKtI9dKBbmi3QP2uPqtus')

nickname = None
year = None

@bot.message_handler(commands=['start'])
def start(message):

    conn = sqlite3.connect('matebase.sql')
    cur = conn.cursor()

    cur.execute('CREATE TABLE IF NOT EXISTS users (id int auto_increment primary key, name varchar(50), yearold varchar(50), name_game varchar(50))')
    conn.commit()
    cur.close()
    conn.close()

    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = types.KeyboardButton('📝Заполнить анкету📝')
    markup.add(btn1)
    bot.send_message(message.from_user.id, "👋Привет! Я помогу найти тебе тиммейта")
    bot.send_message(message.from_user.id, "📝Заполни свою анкету", reply_markup=markup)
    

@bot.message_handler(content_types=['text'])
def add_anketa(message):

    if message.text == '📝Заполнить анкету📝':
        bot.send_message(message.from_user.id, "Как тебя называть?")
        bot.register_next_step_handler(message, user_name)

def user_name(message):
    global nickname
    nickname = message.text.strip()
    bot.send_message(message.from_user.id, "Сколько тебе лет?")
    bot.register_next_step_handler(message, get_year)

def get_year(message):
    global year
    year = message.text.strip()
    bot.send_message(message.from_user.id, "В какие игры ты играешь?")
    bot.register_next_step_handler(message, get_game)

def get_game(message):
    user_game = message.text.strip()
    conn = sqlite3.connect('matebase.sql')
    cur = conn.cursor()

    cur.execute("INSERT INTO users (name, yearold, name_game) VALUES('%s', '%s', '%s')" % (nickname, year, user_game))
    
    conn.commit()
    cur.close()
    conn.close()

    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton('Список пользователей', callback_data='userlist'))
    bot.send_message(message.from_user.id, "Твоя анкета готова!", reply_markup=markup)

@bot.callback_query_handler(func=lambda call: True)
def callback(call):
    conn = sqlite3.connect('matebase.sql')
    cur = conn.cursor()

    cur.execute('SELECT * FROM users')
    user_list = cur.fetchall()

    info = ''
    for el in user_list:
        info += f'Имя: {el[1]}, Возраст: {el[2]}, Во что играю: {el[3]}\n'

    cur.close()
    conn.close()
    bot.send_message(call.message.chat.id, info)


        
       


bot.polling(non_stop= True)