
import os
import telebot
from telebot.types import ReplyKeyboardMarkup, KeyboardButton

TOKEN = os.environ.get("BOT_TOKEN")
bot = telebot.TeleBot(TOKEN)

BOUTIQUES = ["Rauda - 1", "Rauda - 2", "Rauda Rahmet", "Kosmetika"]

def boutique_menu():
    markup = ReplyKeyboardMarkup(resize_keyboard=True)
    for name in BOUTIQUES:
        markup.add(KeyboardButton(name))
    return markup

def action_menu():
    markup = ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add("Добавить продажу")
    markup.add("Сменить бутик")
    return markup

@bot.message_handler(commands=["start"])
def start(message):
    bot.send_message(
        message.chat.id,
        "Выберите бутик:",
        reply_markup=boutique_menu()
    )

@bot.message_handler(func=lambda message: message.text in BOUTIQUES)
def select_boutique(message):
    bot.send_message(
        message.chat.id,
        f"Выбран бутик: {message.text}",
        reply_markup=action_menu()
    )

@bot.message_handler(func=lambda message: message.text == "Сменить бутик")
def change_boutique(message):
    bot.send_message(
        message.chat.id,
        "Выберите другой бутик:",
        reply_markup=boutique_menu()
    )

@bot.message_handler(func=lambda message: message.text == "Добавить продажу")
def add_sale(message):
    bot.send_message(message.chat.id, "Напишите, что продано:")

@bot.message_handler(func=lambda message: True)
def repeat_sale(message):
    bot.send_message(message.chat.id, message.text)

bot.infinity_polling()
