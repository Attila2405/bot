import telebot
from telebot import types
from settings import TG_TOKEN


#=========================================================================================#
#             python calc/calc_bot_2.py
#
#=========================================================================================#

bot = telebot.TeleBot(TG_TOKEN)

calories = 0
proteins = 0
fats = 0
carbohydrates = 0
weight = 0
weight_done = 0
weight_eat = 0
calories_done = 0
proteins_done = 0
fats_done = 0
carbohydrates_done = 0
percent_weight = 0


@bot.message_handler(commands=["start"])
def start(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
    button_beginning = types.KeyboardButton('Старт')
    markup.add(button_beginning)

    mess = f'Привет, {message.from_user.first_name}.'
    bot.send_message(message.chat.id, f"{mess} Это бот для подсчета БЖУ. Для начала нажми Старт", reply_markup=markup)


@bot.message_handler(content_types=["text"])
def beginning(message):
    while True:
        if message.text == 'Старт':
            bot.send_message(message.chat.id, "Введи калорийность сырого продукта на 100гр")
            bot.register_next_step_handler(message, get_calories)
            break
        else:
            photo = open('calc/items/ъуъ.png', 'rb')
            bot.send_photo(message.chat.id, photo)
            bot.send_message(message.chat.id, "Для начала нажми Старт")
            bot.register_next_step_handler(message, beginning)
            break


def get_calories(message):
    global calories
    while True:
        if message.text.isnumeric():
            calories = float(message.text)
            bot.send_message(message.chat.id, 'Введи белки сырого продукта на 100гр')
            bot.register_next_step_handler(message, get_proteins)
            break
        else:
            bot.send_message(message.chat.id, "Введи калорийность сырого продукта на 100гр")
            bot.register_next_step_handler(message, get_calories)
            break


def get_proteins(message):
    global proteins
    while True:
        if message.text.isnumeric():
            proteins = float(message.text)
            bot.send_message(message.chat.id, 'Введи жиры сырого продукта на 100гр')
            bot.register_next_step_handler(message, get_fats)
            break
        else:
            bot.send_message(message.chat.id, 'Введи белки сырого продукта на 100гр')
            bot.register_next_step_handler(message, get_proteins)
            break


def get_fats(message):
    global fats
    while True:
        if message.text.isnumeric():
            fats = float(message.text)
            bot.send_message(message.chat.id, 'Введи углеводы сырого продукта на 100гр')
            bot.register_next_step_handler(message, get_carbohydrates)
            break
        else:
            bot.send_message(message.chat.id, 'Введи жиры сырого продукта на 100гр')
            bot.register_next_step_handler(message, get_fats)
            break


def get_carbohydrates(message):
    global carbohydrates
    while True:
        if message.text.isnumeric():
            carbohydrates = float(message.text)
            bot.send_message(message.chat.id, 'Введи вес сырого продукта который хотите приготовить')
            bot.register_next_step_handler(message, get_weight)
            break
        else:
            bot.send_message(message.chat.id, 'Введи углеводы сырого продукта на 100гр')
            bot.register_next_step_handler(message, get_carbohydrates)
            break


def get_weight(message):
    global weight
    while True:
        if message.text.isnumeric():
            weight = float(message.text)
            bot.send_message(message.chat.id, 'Введи вес готового продукта')
            bot.register_next_step_handler(message, get_weight_done)
            break
        else:
            bot.send_message(message.chat.id, 'Введи вес сырого продукта который хотите приготовить')
            bot.register_next_step_handler(message, get_weight)
            break


def get_weight_done(message):
    global weight, weight_done, calories_done, proteins_done, carbohydrates_done, fats_done, percent_weight
    while True:
        if message.text.isnumeric():
            weight_done = float(message.text)
            if weight < weight_done:
                percent_weight = round(abs((weight_done - weight) / weight_done), 3)
            else:
                percent_weight = round(abs((weight - weight_done) / weight_done), 3)
            # bot.send_message(message.from_user.id, 'Процентное изменение веса в числовом виде ' + str(percent_weight))
            if weight > weight_done:
                calories_done = round(calories + (calories * percent_weight), 1)
                proteins_done = round(proteins + (proteins * percent_weight), 1)
                carbohydrates_done = round(carbohydrates + (carbohydrates * percent_weight), 1)
                fats_done = round(fats + (fats * percent_weight), 1)
            else:
                calories_done = abs(round(calories - (calories * percent_weight), 1))
                proteins_done = abs(round(proteins - (proteins * percent_weight), 1))
                carbohydrates_done = abs(round(carbohydrates - (carbohydrates * percent_weight), 1))
                fats_done = abs(round(fats - (fats * percent_weight), 1))
            bot.send_message(message.chat.id, f'На 100 гр. готового продукта - {calories_done} калорий, \
 {proteins_done} белка, {fats_done} жиров, {carbohydrates_done} углеводов')
            bot.send_message(message.chat.id, 'Введи сколько продукта хотите сьесть')
            bot.register_next_step_handler(message, get_weight_eat)
            break
        else:
            bot.send_message(message.chat.id, 'Введи вес готового продукта')
            bot.register_next_step_handler(message, get_weight_done)
            break


def get_weight_eat(message):
    global weight_eat, calories_done, proteins_done, carbohydrates_done, fats_done, percent_weight
    while True:
        if message.text.isnumeric():
            weight_eat = float(message.text)
            calories_eat = round((calories_done / 100) * weight_eat, 1)
            proteins_eat = round((proteins_done / 100) * weight_eat, 1)
            carbohydrates_eat = round((carbohydrates_done / 100) * weight_eat, 1)
            fats_eat = round((fats_done / 100) * weight_eat, 1)
            bot.send_message(message.chat.id, f'На {weight_eat} гр. готового продукта - {calories_eat} калорий, \
 {proteins_eat} белка, {fats_eat} жиров, {carbohydrates_eat} углеводов')
            break
        else:
            bot.send_message(message.chat.id, 'Введи сколько продукта хотите сьесть')
            bot.register_next_step_handler(message, get_weight_eat)
            break


def restart(message):
    bot.send_message(message.chat.id, 'Если хочешь заново посчитать КБЖУ нажми Старт')


bot.polling(none_stop=True)
