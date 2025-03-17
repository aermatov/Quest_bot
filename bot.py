from telebot import TeleBot
from telebot.types import InlineKeyboardButton, InlineKeyboardMarkup

from stage_texts import (
    STAGE_FIRST_TEXT,
    STAGE_SECOND_TEXT,
    STAGE_THIRD_TEXT,
    STAGE_FOURTH_TEXT,
    STAGE_FIFTH_TEXT,
    STAGE_SIXTH_TEXT
)

from utils import random_choice_answer


bot = TeleBot("8068560009:AAGwCHiBIZimKttwErd6o28RdM8LEWvVL4s")

user_hp = {}

def update_hp(user_id, amound):
    if user_id not in user_hp:
        user_hp[user_id] = 3

    user_hp[user_id] += amound
    if user_hp[user_id] <= 0:
        return 'GAME OVER'
    else:
        return f'Осталось {user_hp[user_id]} попыток'


@bot.message_handler(commands=["start",])
def first_stage(message):
    user_hp[message.chat.id] = 3
    text = STAGE_FIRST_TEXT
    markup = InlineKeyboardMarkup()
    markup.add(
        InlineKeyboardButton(
            "Подойти к монитору и попробовать разобраться",
            callback_data="second_stage"
        )
    )
    markup.add(
        InlineKeyboardButton(
            "Попробовать вскрыть панель замка вручную",
            callback_data="third_stage"
        )
    )
    markup.add(
        InlineKeyboardButton(
            "Осмотреть комнату в поисках улик",
            callback_data="fourth_stage"
        )
    )
    bot.send_message(message.chat.id, text=text, reply_markup=markup)

@bot.callback_query_handler(func=lambda call: call.data == "second_stage")
def second_stage(call):
    text = STAGE_SECOND_TEXT
    bot.send_message(call.message.chat.id, text=text)

@bot.message_handler()
def get_second_stage_answer(message):
    global user_hp
    if message.text.lower() == "часы":
        markup = InlineKeyboardMarkup()
        markup.add(
            InlineKeyboardButton("Пройти дальше", callback_data="fifth_stage")
        )
        bot.send_message(
            message.chat.id,
            text="Правильно! Проходишь дальше",
            reply_markup=markup
        )
    else:
        result = update_hp(message.chat.id, -1)
        if result == 'GAME OVER':
            bot.send_message(message.chat.id, text = 'GAME OVER')
        else:
            bot.send_message(message.chat.id, text = result)

@bot.callback_query_handler(func=lambda call: call.data == "third_stage")
def third_stage(call):
    text = STAGE_THIRD_TEXT
    markup = InlineKeyboardMarkup()
    markup.add(
        InlineKeyboardButton(
            "Красный провод",
            callback_data="red_wire"
        )
    )
    markup.add(
        InlineKeyboardButton(
            "Синий провод",
            callback_data="fifth_stage"
        )
    )
    markup.add(
        InlineKeyboardButton(
            "Желтый провод",
            callback_data="fourth_stage"
        )
    )
    bot.send_message(call.message.chat.id, text=text, reply_markup=markup)

@bot.callback_query_handler(func=lambda call: call.data == "red_wire")
def hp_red_wire(call):
    global user_hp
    result = update_hp(call.message.chat.id, -1)
    if result == 'GAME OVER':
        bot.send_message(call.message.chat.id, text='GAME OVER')
    else:
        bot.send_message(call.message.chat.id, text=f'Тревога!!!\n{result}')

@bot.callback_query_handler(func=lambda call: call.data == "fourth_stage")
def fourth_stage(call):
    text = STAGE_FOURTH_TEXT
    markup = InlineKeyboardMarkup()
    markup.add(
        InlineKeyboardButton(
            "Вернуться к монитору и ввести «12:00»",
            callback_data="fifth_stage"
        )
    )
    markup.add(
        InlineKeyboardButton(
            "Проигнорировать и вернуться к замку",
            callback_data="third_stage"
        )
    )
    bot.send_message(call.message.chat.id, text=text, reply_markup=markup)

@bot.callback_query_handler(func=lambda call: call.data == "fifth_stage")
def fifth_stage(call):
    text = STAGE_FIFTH_TEXT
    markup = InlineKeyboardMarkup()
    markup.add(
        InlineKeyboardButton("Потянуть левый рычаг", callback_data="sixth_stage")
    )
    markup.add(
        InlineKeyboardButton("Потянуть правый рычаг", callback_data="red_wire")
    )
    markup.add(
        InlineKeyboardButton(
            " Попробовать проскользнуть между лазерами ",
            callback_data="random_choice"
        )
    )
    bot.send_message(call.message.chat.id, text=text, reply_markup=markup)

@bot.callback_query_handler(func=lambda call: call.data == "random_choice")
def random_choice(call):
    result, text = random_choice_answer()
    bot.send_message(call.message.chat.id, text=text)

    if text == "Вам улыбнулась удача! Проходите дальше":
        sixth_stage(call)
    elif text == "Упс":
        left_door(call)

@bot.callback_query_handler(func=lambda call: call.data == "sixth_stage")
def sixth_stage(call):
    text = STAGE_SIXTH_TEXT
    markup = InlineKeyboardMarkup()
    markup.add(
        InlineKeyboardButton(
            "Левая дверь", callback_data="left_door"  # Добавлен callback_data
        )
    )
    markup.add(
        InlineKeyboardButton(
            "Правая дверь", callback_data="right_door"  # Добавлен callback_data
        )
    )
    bot.send_message(call.message.chat.id, text=text, reply_markup=markup)

@bot.callback_query_handler(func=lambda call: call.data == "left_door")
def left_door(call):
    result = update_hp(call.message.chat.id, -user_hp.get(call.message.chat.id, 0))

    if result == "GAME OVER":
        bot.send_message(call.message.chat.id, text="GAME OVER")
    else:
        bot.send_message(call.message.chat.id, text=result)

@bot.callback_query_handler(func=lambda call: call.data == "right_door")
def right_door(call):
    bot.send_message(call.message.chat.id, 'VICTORY')

bot.infinity_polling()
