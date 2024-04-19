import telebot
from telebot import types
import requests
import json
import time
import sqlite3

bot = telebot.TeleBot("7034632826:AAH65MjuQIkXKTU_AbOyuj6jNeHM6QPTAtU")
API = '8a6d92239deea00140d3d903f309c5d6'
@bot.message_handler(commands=['start'])
def start_func(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    button1 = types.KeyboardButton("Добавить город / Изменить город")
    markup.add(button1)
    bot.send_message(message.chat.id, f'Привет, {message.from_user.first_name}, Я бот который сообщает о том что через час начинается дождь'.format(message.from_user), reply_markup=markup)


@bot.message_handler(content_types=["text"])
def сheck_messages(message):
    if(message.text == "Добавить город / Изменить город"):
        bot.send_message(message.chat.id, f'Напиши название своего Города')
        bot.register_next_step_handler(message, get_city)
    

def get_city(message):
    global city
    city = message.text.strip().lower()
    result = requests.get(f'https://api.openweathermap.org/data/2.5/weather?q={city}&appid={API}&units=metric')
    if result.status_code == 200:
        bot.send_message(message.chat.id, f'Твой город это {city.capitalize()}, я сообщу если надвигается дождь')
        while True:
            get_weather(message)
            time.sleep(3600)
    else:
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        button1 = types.KeyboardButton("Добавить город / Изменить город")
        markup.add(button1)
        bot.send_message(message.chat.id, f"Город указан не верно".format(message.from_user), reply_markup=markup)

def get_weather(message):
    result = requests.get(f'https://api.openweathermap.org/data/2.5/weather?q={city}&appid={API}&units=metric')
    weather_data = json.loads(result.text)
    bot.send_message(message.chat.id, weather_data['weather'][0]['main'].lower())
    if weather_data['weather'][0]['main'].lower() != "rain":
        result_hour = requests.get(f"https://api.openweathermap.org/data/2.5/forecast?q={city}&appid={API}&units=metric")
        weather_data_1 = json.loads(result_hour.text)
        weather_description = weather_data_1['list'][0]['weather'][0]['main']
        bot.send_message(message.chat.id, f'через час будет {weather_description.lower()}')
        if weather_description.lower() == "rain":
            bot.send_message(message.chat.id, 'Через час будет дождь')

bot.polling(none_stop=True)