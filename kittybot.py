# kittybot/kittybot.py
import os
import logging


import requests


from telegram.ext import Updater, Filters, MessageHandler, CommandHandler
from telegram import ReplyKeyboardMarkup

from dotenv import load_dotenv

load_dotenv()

TOKEN = os.getenv('TOKEN_BOT')

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO,
    filename='main.log'
    )

URL = 'https://api.thecatapi.com/v1/images/search'

def get_new_image():
    try:
        response = requests.get(URL)
    except Exception as error:
        logging.error(f'Ошибка при запросе к основному API: {error}')
        new_url = 'https://api.thedogapi.com/v1/images/search'
        response = requests.get(new_url)

    response = response.json()
    random_cat = response[0].get('url')
    return random_cat

def new_cat(update, context):
    chat = update.effective_chat
    context.bot.send_photo(
        chat.id, 
        get_new_image())

def wake_up(update, context):
    chat = update.effective_chat
    name = update.message.chat.first_name
    button = ReplyKeyboardMarkup([['Новый котик']], resize_keyboard=True)

    context.bot.send_message(
        chat_id=chat.id, 
        text='Привет, {}. Посмотри, какого котика я тебе нашёл'.format(name),
        reply_markup=button
        )

    context.bot.send_photo(chat.id, get_new_image())

def main():
    updater = Updater(TOKEN)

    updater.dispatcher.add_handler(CommandHandler('start', wake_up))
    updater.dispatcher.add_handler(MessageHandler(Filters.text, new_cat))

    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()