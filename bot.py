import telebot
from commands import commands, hidden as hid
import requests
import json
import os

from user import User
from anime_standalone import get_anime
from kanc_ship import get_ship, strongest_by_class

TOKEN = ''

bot = telebot.TeleBot(TOKEN)
users = []

@bot.message_handler(commands=['start'])
def start(message):
    for user in users:
        if str(user) == str(message.chat.id):
            bot.send_message(message.chat.id, 'Кулити, ' + user.name)
            return
    
    sent = bot.send_message(message.chat.id, 'Кулити, как звать то?')
    bot.register_next_step_handler(sent, hello)

def hello(message):
    bot.reply_to(message, 'Кулити, {name}.'.format(name=message.text))
    user = User(message.text, message.chat.id)
    users.append(user)
    with open('sessions/' + str(message.chat.id) + '.txt', 'w') as file:
        json.dump(user.form_json(), file)

@bot.message_handler(commands=['help'])
def help(message):
    for user in users:
        if str(user) == str(message.chat.id):
            msg = ''
            for key in commands:
                msg += key + ' - ' + commands[key] + '\n'
            bot.send_message(message.chat.id, 'Ну смотри, короч\n' + msg)
            return
    
    bot.send_message(message.chat.id, 'Сначала /start уй или пиздуй')
    

@bot.message_handler(commands=['happy'])
def happy(message):
    img = open('alway.jpg', 'rb')
    bot.send_photo(message.chat.id, img)

@bot.message_handler(commands=['anime_suggest'])
def anime_suggest(message):
    bot.send_message(message.chat.id, 'Boku no Pico')
    bot.send_message(message.chat.id, 'http://bit.ly/2eU7XTz')

@bot.message_handler(commands=['random'])
def random(message):
    bot.send_photo(message.chat.id, 'https://myanimelist.cdn-dena.com/images/anime/6/88286.jpg')

@bot.message_handler(regexp=r'Ярик пидор')
def pidor(message):
    bot.reply_to(message, 'Тут соглы+++')

@bot.message_handler(commands=['add_mal'])
def add_mal(message):
    for user in users:
        if str(user) == str(message.chat.id):
            if not user.mal == None:
                bot.send_message(message.chat.id, 'Текущий логин - ' + user.mal)
            sent = bot.send_message(message.chat.id, 'Логин?')
            bot.register_next_step_handler(sent, reg_mal)
            return

    start(message)
    

def reg_mal(message):
    if requests.get('https://myanimelist.net/animelist/' + message.text).status_code == 404:
        bot.send_message(message.chat.id, 'Ты шо долбоёб? Нет такого пользователя')
        return
    
    for user in users:
        if str(user) == str(message.chat.id):
            user.mal = message.text
            with open('sessions/' + str(message.chat.id) + '.txt', 'w') as file:
                json.dump(user.form_json(), file)
            
    bot.send_message(message.chat.id, 'Готово')

@bot.message_handler(commands=['anime_watching'])
def show_list(message):

    for user in users:
        if str(user) == str(message.chat.id):
            if user.mal == None:
                bot.send_message(message.chat.id, 'Нет логина, зарегаться? /add_mal')
                return
            
            bot.send_message(message.chat.id, 'Работает папсназ')

            for i in get_anime(user.mal):
                bot.send_message(message.chat.id, i)

            return

    start(message)

@bot.message_handler(commands=['hidden'])
def hidden(message):
    msg = ''
    for h in hid:
        msg += h + '\n'
    bot.send_message(message.chat.id, 'Скрытые фичи для разумистов\n' + msg)

@bot.message_handler(regexp=r'.*Навальн.*')
def nav(message):
    bot.send_message(message.chat.id, '20!8')  
    
def error_message(message):
    bot.send_message(message.chat.id, 'Что-то пошло не так, повторите команду')


files = [f for f in os.listdir('sessions/')]
for f in files:
    with open('sessions/'+ f) as file:
        data = json.load(file)
        users.append(User(data['name'], str(f).rsplit('.', 1)[0], data['mal']))
            

@bot.message_handler(commands=['get_ship'])
def ship(message):
    sent = bot.send_message(message.chat.id, "Ship name?")
    bot.register_next_step_handler(sent, ship_data)

def ship_data(message):
    for i in get_ship(message.text):
        bot.send_message(message.chat.id, i)


@bot.message_handler(commands=['get_strongest_ship'])
def ship(message):
    sent = bot.send_message(message.chat.id, "Ship class?")
    bot.register_next_step_handler(sent, ship_strongest)

def ship_strongest(message):
    bot.send_message(message.chat.id, strongest_by_class(message.text))

bot.polling()
