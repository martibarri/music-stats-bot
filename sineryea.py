import logging
import requests
import urllib

from os import getenv
from datetime import datetime, timedelta
from pathlib import Path
from dotenv import load_dotenv
from aiogram import Bot, Dispatcher, executor, types
from aiogram.utils.markdown import hbold
from social_utils import get_followers_twitter, get_followers_insta, get_followers_facebook, get_followers_spotify, get_followers_youtube
from spotify_utils import search_spotify, formatted_playlist, pretty_playlist


# Load environment variables
load_dotenv()
API_TOKEN = getenv('API_TOKEN')
CHATID = getenv('CHATID')
ACCESS_TOKEN = getenv('ACCESS_TOKEN')
LOGGING_PATH = getenv('LOGGING_PATH', 'logs')
LOGGING_FILE = getenv('LOGGING_FILE')
YOUR_API_KEY = getenv('YOUR_API_KEY')

# Configure logging
if LOGGING_FILE:
    Path(LOGGING_PATH).mkdir(parents=True, exist_ok=True)
    logging.basicConfig(
        level=logging.INFO,
        filename=Path(LOGGING_PATH) / Path(LOGGING_FILE),
        filemode='a',
        format='%(asctime)s.%(msecs)03d\t%(levelname)s\t%(name)s\t%(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
else:
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s.%(msecs)03d\t%(levelname)s\t%(name)s\t%(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )


# Initialize bot and dispatcher
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)


MY_DB = {
    'last_date': None,
    'fb': None,
    'insta': None,
    'tw': None,
    'sp': None,
    'yt': None,
}


def send_message(msg):
    parsedmsg = urllib.parse.quote_plus(msg)
    requests.get(f"https://api.telegram.org/bot{API_TOKEN}/sendMessage?chat_id={CHATID}&text={parsedmsg}")


@dp.message_handler(regexp='(xarx|social|xs|seguidor|follow|subscri|informaci|stats)')
async def info_xxss(message: types.Message):
    global MY_DB
    now = datetime.utcnow()
    # First scan or rescan + update values
    if (not MY_DB['last_date']) or (now > MY_DB['last_date'] + timedelta(hours=12)):
        # first scan
        MY_DB['fb'] = get_followers_facebook('sinergiareggae')
        MY_DB['insta'] = get_followers_insta('sinergiareggae')
        MY_DB['tw'] = get_followers_twitter(ACCESS_TOKEN, 'sinergiareggae')
        MY_DB['sp'] = get_followers_spotify()
        MY_DB['yt'] = get_followers_youtube(YOUR_API_KEY)
        MY_DB['last_date'] = now
    # Print message
    msg = f"🕸 {hbold('Sinergia stats')} 🕸"
    msg += f"\nFacebook: {hbold(MY_DB['fb'])}" if MY_DB['fb'] else ''
    msg += f"\nInstagram: {hbold(MY_DB['insta'])}" if MY_DB['insta'] else ''
    msg += f"\nTwitter: {hbold(MY_DB['tw'])}" if MY_DB['tw'] else ''
    msg += f"\nSpotify: {hbold(MY_DB['sp'])}" if MY_DB['sp'] else ''
    msg += f"\nYoutube: {hbold(MY_DB['yt'])}" if MY_DB['yt'] else ''
    msg += f"\nUpdated: {MY_DB['last_date'].strftime('%Y-%m-%d %H:%M:%S')}" if MY_DB['last_date'] else ''
    logging.info(msg)
    await message.answer(msg, parse_mode='html')


@dp.message_handler(commands=['playlist'])
async def search_playlist(message: types.Message):
    """
    This handler will be called when user sends `/playlist` command
    """
    arguments = message.get_args()
    if arguments:
        query = arguments
    else:
        await message.answer(f'usage: /playlist TEXT TO SEARCH')
        return

    ##########################
    query += " NOT reggaeton"
    limit_search = 20
    minim_followers = 200
    search_type = 'playlist'
    market = 'ES'
    ##########################

    logging.info(f"query: {query} by user {types.User.get_current()}")

    playlists = search_spotify(search_type, query, limit_search, market)

    pretty_playlists = []
    for p in playlists:
        if p['followers']['total'] > minim_followers:
            f = formatted_playlist(p)
            logging.info(f)
            p = pretty_playlist(f)
            await message.answer(p, parse_mode='html', disable_web_page_preview=True)
            pretty_playlists.append(p)

    search_result = f'{len(pretty_playlists)} relevant results of {len(playlists)} response results'
    logging.info(search_result)
    await message.answer(search_result)


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=False)
