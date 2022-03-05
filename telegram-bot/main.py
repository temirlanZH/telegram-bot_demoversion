#Стандартные Модули
from datetime import datetime as dt

# Сторонние модули
from telebot import TeleBot
from telebot.types import (CallbackQuery, InlineKeyboardMarkup,
                             InlineKeyboardButton, Message)

# Локальные Модули
import bot_token
import welcome_handler as w_handler

# Bot Initialization
bot = TeleBot(bot_token.token)

# Variables
bot.w_file = "animation"

@bot.message_handler(commands=["start"])
def welcome(message: Message) -> None:

    file_path = _choose_welcome_file()

    if bot.w_file != "text": 
        with open(file_path, "rb") as file:
            if bot.w_file == "photo":
                bot.send_photo(message.chat.id, file)
            elif bot.w_file == "sticker" or bot.w_file == "animated":
                bot.send_sticker(message.chat.id, file)
            elif bot.w_file == "animation":
                bot.send_animation(message.chat.id, file)

    msg_text = w_handler.prep_cmd_msg(message)
    
    bot.send_message(message.chat.id, msg_text)

def _choose_welcome_file() -> str:
    if bot.w_file == "photo":
        file_path = "static/menhera.webp"
    elif bot.w_file == "sticker":
        file_path = "static/sticker.webp"
    elif bot.w_file == "animatied":
        file_path = "static/stick.webp"
    elif bot.w_file == "animation":
        file_path = "static/happy-anime.mp4"

    return file_path

@bot.message_handler(commands=["help"])
def help(message: Message) -> None:

    msg_text = w_handler.prep_cmd_msg(message)

    bot.send_message(message.chat.id, msg_text)



@bot.message_handler(commands=["config"])
def config(message: Message) -> None:

    config_keyboard = InlineKeyboardMarkup(row_width=2)

    photo_key = InlineKeyboardButton(text="Photo + Text",
                                     callback_data="photo")
    animation_key = InlineKeyboardButton(text="Animation + Text",
                                     callback_data="animation")
    sticker_key = InlineKeyboardButton(text="Sticker + Text",
                                     callback_data="sticker")
    text_key = InlineKeyboardButton(text="Only text",
                                     callback_data="text")

    config_keyboard.add(photo_key, animation_key, sticker_key, text_key)

    bot.send_message(message.chat.id, " {0.first_name} Select greeting type!".format(message.from_user),
                    reply_markup=config_keyboard)


def _sticker_type(message: Message) -> None:

    sticker_keyboard = InlineKeyboardMarkup(row_width=2)

    standard_key = InlineKeyboardButton(text = "Simple sticker",
                                        callback_data="standard")

    anim_key = InlineKeyboardButton(text = "animated sticker", 
                                    callback_data="animated")


    sticker_keyboard.add(standard_key, anim_key)

    bot.send_message(message.chat.id, "Choose sticker type!",
                        reply_markup=sticker_keyboard)

@bot.callback_query_handler(func=lambda call:True)
def callback_query(call: CallbackQuery) -> None:

    bot.answer_callback_query(call.id)

    if call.data == "photo":
        bot.w_file = "photo"
        _send_anim(call)
    if call.data == "animation":
        bot.w_file = "animation"
        _send_anim(call)
    if call.data == "sticker":
        _sticker_type(call.message)
    if call.data == "text":
        bot.w_file = "text"
        _send_anim(call)
    if call.data == "standard":
        bot.w_file = "sticker"
        _send_anim(call)
    if call.data == "animated":
        bot.w_file = "animated"
        _send_anim(call)

def _send_anim(call: CallbackQuery) -> None:
    with open("static/anim.webp", "rb") as sticker:
        bot.send_sticker(call.message.chat.id, sticker)

bot.polling(none_stop=True, interval=0)