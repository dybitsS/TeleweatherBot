import telebot
from telebot import types
import requests
import json
import time

bot = telebot.TeleBot("7034632826:AAH65MjuQIkXKTU_AbOyuj6jNeHM6QPTAtU")
API = '8a6d92239deea00140d3d903f309c5d6'
@bot.message_handler(commands=['start'])
def start_func(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    button1 = types.KeyboardButton("Добавить Город")
    markup.add(button1)
    bot.send_message(message.chat.id, f'Привет, {message.from_user.first_name}, Я бот который сообщает о том что через час начинается дождь'.format(message.from_user), reply_markup=markup)


@bot.message_handler(content_types=["text"])
def сheck_messages(message):
    if(message.text == "Добавить Город"):
        bot.send_message(message.chat.id, f'Напиши название своего Города')
        bot.register_next_step_handler(message, get_city)
        
    # if(message.text == "Узнать погоду"):
    #     bot.register_next_step_handler(message, get_weather)
    

def get_city(message):
    global city
    city = message.text.strip().lower()
    result = requests.get(f'https://api.openweathermap.org/data/2.5/weather?q={city}&appid={API}&units=metric')
    if result.status_code == 200:
        bot.send_message(message.chat.id, f'Твой город это {city}')
        while True:
            get_weather(message)
            time.sleep(3600)
    else:
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        button1 = types.KeyboardButton("Добавить Город")
        markup.add(button1)
        bot.send_message(message.chat.id, f"Город указан не верно".format(message.from_user), reply_markup=markup)
    # markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    # button1 = types.KeyboardButton("Узнать погоду")
    # markup.add(button1)
    # bot.send_message(message.chat.id, "Теперь ты можешь узнать погоду".format(message.from_user), reply_markup=markup)

def get_weather(message):
    result = requests.get(f'https://api.openweathermap.org/data/2.5/weather?q={city}&appid={API}&units=metric')
    weather_data = json.loads(result.text)
    if weather_data['weather'][0]['main'].lower() != "rain":
        result_hour = requests.get(f"https://api.openweathermap.org/data/2.5/forecast?q={city}&appid={API}&units=metric")
        weather_data_1 = json.loads(result_hour.text)
        weather_description = weather_data_1['list'][0]['weather'][0]['description']  
        if weather_description.lower() == "rain":
            bot.send_message(message.chat.id, 'Через час будет дождь')
    

# def check_if_soon_rain(message):
#     result_hour = requests.get(f"https://api.openweathermap.org/data/2.5/forecast?q={city}&appid={API}&units=metric")
#     weather_data_1 = json.loads(result_hour.text)
#     weather_description = weather_data_1['list'][0]['weather'][0]['description']
#     if weather_description == "rain":
#         bot.send_message(message.chat.id, 'Через час будет дождь')

# while True:
#     get_weather(message)
#     time.sleep(3600)

bot.polling(none_stop=True)