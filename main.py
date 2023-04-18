import logging

import telegram
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
import random

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

updater = Updater(token='6288578263:AAFmSFsmyv5MYP68M_n71iHUagP1K--wZR4', use_context=True)
dispatcher = updater.dispatcher


def start(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text="Telefon modelini tanlang.")
    context.user_data['phone'] = ['Redmi', 'Samsung', 'Oppo', 'Iphone']
    keyboard = [[f"{car}"] for car in context.user_data['phone']]
    reply_markup = {'keyboard': keyboard, 'one_time_keyboard': True}
    context.bot.send_message(chat_id=update.effective_chat.id, text='Telefon turini tanlang', reply_markup=reply_markup)


def select_car(update, context):
    selected_phone = update.message.text
    context.user_data['selected_phone'] = selected_phone
    context.bot.send_message(chat_id=update.effective_chat.id, text=f"{selected_phone} tanlandi.")


def send_contact(update, context):
    user_contact = update.message.contact.phone_number
    context.user_data['contact'] = user_contact
    context.bot.send_message(chat_id=update.effective_chat.id, text="Hozir qayerdasiz?")
    context.bot.send_message(chat_id=update.effective_chat.id, text="Locationingizni yuboring",
                             reply_markup=telegram.KeyboardButton(text="Share Location", request_location=True))


def send_location(update, context):
    user_location = update.message.location
    context.user_data['location'] = user_location
    context.bot.send_message(chat_id=update.effective_chat.id, text="Qabul qilindi!")


def get_random_car_number(update, context):
    selected_car = context.user_data['selected_car']
    car_number = "Random Mashina Raqami: " + str(random.randint(1000, 9999))
    context.bot.send_message(chat_id=update.effective_chat.id, text=car_number)
    context.bot.send_message(chat_id=update.effective_chat.id, text="Raqamni yuboring",
                             reply_markup=telegram.KeyboardButton(text="Send Contact", request_contact=True))


start_handler = CommandHandler('start', start)
select_car_handler = MessageHandler(Filters.text & ~Filters.command, select_car)
send_contact_handler = MessageHandler(Filters.contact, send_contact)
send_location_handler = MessageHandler(Filters.location, send_location)
get_random_car_number_handler = MessageHandler(Filters.regex('^(Redmi|Samsung|Oppo|Iphone)$'), get_random_car_number)

dispatcher.add_handler(start_handler)
dispatcher.add_handler(select_car_handler)
dispatcher.add_handler(send_contact_handler)
dispatcher.add_handler(send_location_handler)
dispatcher.add_handler(get_random_car_number_handler)

updater.start_polling()