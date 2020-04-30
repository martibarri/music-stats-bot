import logging
import bs4
import requests
import urllib
import json


from os import getenv
from dotenv import load_dotenv
from aiogram import Bot, Dispatcher, executor, types

from social_utils import get_followers_twitter, get_followers_insta, get_followers_facebook


# Load environment variables
load_dotenv()
API_TOKEN = getenv('API_TOKEN')
CHATID = getenv('CHATID')
ACCESS_TOKEN = getenv('ACCESS_TOKEN')
LOGGING_FILE = bool(getenv('LOGGING_FILE') == 'True')

# Configure logging
if LOGGING_FILE:
    logging.basicConfig(
        level=logging.INFO,
        filename='sineryea.log',
        filemode='a',
        format='%(asctime)s,%(msecs)d %(name)s %(levelname)s %(message)s',
        datefmt='%H:%M:%S'
    )
else:
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s,%(msecs)d %(name)s %(levelname)s %(message)s',
        datefmt='%H:%M:%S'
    )


# Initialize bot and dispatcher
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)


def send_message(msg):
    parsedmsg = urllib.parse.quote_plus(msg)
    requests.get(f"https://api.telegram.org/bot{API_TOKEN}/sendMessage?chat_id={CHATID}&text={parsedmsg}")


@dp.message_handler(regexp='(^insta)')
async def info(message: types.Message):
    followers = get_followers_insta('sinergiareggae')
    msg = f"Tenim {followers} followers a Instragram 😊"
    logging.info(msg)
    await message.answer(msg)


@dp.message_handler(regexp='(^twitter)')
async def info(message: types.Message):
    followers = get_followers_twitter('sinergiareggae')
    msg = f"Tenim {followers} followers a Twitter 😊"
    logging.info(msg)
    await message.answer(msg)


@dp.message_handler(regexp='(^face)')
async def info(message: types.Message):
    followers = get_followers_facebook('sinergiareggae')
    msg = f"Tenim {followers} followers a Facebook 😊"
    logging.info(msg)
    await message.answer(msg)


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=False)
