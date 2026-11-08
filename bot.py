
import os
import telebot
from flask import Flask, request
from telebot.types import ReplyKeyboardMarkup, KeyboardButton

TOKEN = os.environ["BOT_TOKEN"]
bot = telebot.TeleBot(TOKEN)
app = Flask(__name__)

BOUTIQUES = ["Rauda - 1", "Rauda - 2", "Rauda Rahmet", "Kosmetika"]
selected = {}
awaiting_sale = set()

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
    selected.pop(message.chat.id, None)
    awaiting_sale.discard(message.chat.id)
    bot.send_message(message.chat.id, "Выберите бутик:", reply_markup=boutique_menu())

@bot.message_handler(func=lambda m: m.text in BOUTIQUES)
def choose_boutique(message):
    selected[message.chat.id] = message.text
    awaiting_sale.discard(message.chat.id)
    bot.send_message(
        message.chat.id,
        f"Выбран бутик: {message.text}",
        reply_markup=action_menu()
    )

@bot.message_handler(func=lambda m: m.text == "Сменить бутик")
def change_boutique(message):
    awaiting_sale.discard(message.chat.id)
    bot.send_message(message.chat.id, "Выберите бутик:", reply_markup=boutique_menu())

@bot.message_handler(func=lambda m: m.text == "Добавить продажу")
def add_sale(message):
    if message.chat.id not in selected:
        bot.send_message(message.chat.id, "Сначала выберите бутик.", reply_markup=boutique_menu())
        return
    awaiting_sale.add(message.chat.id)
    bot.send_message(message.chat.id, "Напишите, что продано:")

@bot.message_handler(content_types=["text"])
def repeat_sale(message):
    chat_id = message.chat.id

    if chat_id not in awaiting_sale:
        bot.send_message(chat_id, "Выберите действие:", reply_markup=action_menu() if chat_id in selected else boutique_menu())
        return

    boutique = selected.get(chat_id, "Не выбран")
    awaiting_sale.discard(chat_id)

    bot.send_message(
        chat_id,
        f"Бутик: {boutique}\n\n{message.text}",
        reply_markup=action_menu()
    )

@app.route("/", methods=["GET"])
def home():
    return "Parfum Cash Bot is running!"

@app.route("/webhook", methods=["POST"])
def webhook():
    update = telebot.types.Update.de_json(request.get_data().decode("utf-8"))
    bot.process_new_updates([update])
    return "OK", 200

if os.environ.get("RENDER_EXTERNAL_URL"):
    bot.remove_webhook()
    bot.set_webhook(url=os.environ["RENDER_EXTERNAL_URL"] + "/webhook")
