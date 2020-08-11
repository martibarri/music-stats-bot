import logging
import requests
import urllib

from os import getenv, path, listdir
from secrets import choice
from datetime import datetime, timedelta
from pathlib import Path
from dotenv import load_dotenv
from aiogram import Bot, Dispatcher, executor, types
from aiogram.utils.markdown import hbold, hitalic
from social_utils import get_followers_twitter, get_followers_instagram, get_followers_facebook, get_followers_spotify, get_followers_youtube
from spotify_utils import search_spotify, formatted_playlist, pretty_playlist


# Load environment variables
load_dotenv()
LOGGING_PATH = getenv('LOGGING_PATH', 'logs')
LOGGING_FILE = getenv('LOGGING_FILE')
API_TOKEN = getenv('API_TOKEN')  # Telegram
MY_CHATID = getenv('MY_CHATID')  # Telegram
ACCESS_TOKEN = getenv('ACCESS_TOKEN')  # Twitter
YOUR_API_KEY = getenv('YOUR_API_KEY')  # Youtube
ALLOW_LIST_CHATIDS = list(map(int, getenv('ALLOW_LIST_CHATIDS').split(',')))  # Telegram

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


# Set the name of public accounts
accounts = {
    'music_group_name': 'Sinergia',
    'facebook': 'sinergiareggae',
    'instagram': 'sinergiareggae',
    'twitter': 'sinergiareggae',
    'spotify': '6i0i8gXIR3RQRnfWvRWrPa',
    'youtube': 'UCsR3pSI6iRNlxyFkqmJ1tGg',
}

SOCIAL_UPDATE_TIME = 12  # in hours

MY_DB = {
    'last_date': None,
    'facebook': None,
    'instagram': None,
    'twitter': None,
    'spotify': None,
    'youtube': None,
}


def restricted(func):
    def func_wrapper(f):
        logging.info(f)
        chat_id = f['chat']['id']
        if chat_id in ALLOW_LIST_CHATIDS:
            return func(f, True)
        else:
            return func(f, False)
    return func_wrapper


def send_message(msg):
    parsedmsg = urllib.parse.quote_plus(msg)
    requests.get(f"https://api.telegram.org/bot{API_TOKEN}/sendMessage?chat_id={MY_CHATID}&text={parsedmsg}")


@dp.message_handler(regexp='(xarx|social|xs|seguidor|follow|subscri|informaci|stats)')
@restricted
async def info_xxss(message: types.Message, allowed):
    if allowed:
        global MY_DB
        now = datetime.utcnow()
        # First scan or rescan + update values
        if (not MY_DB['last_date']) or (now > MY_DB['last_date'] + timedelta(hours=SOCIAL_UPDATE_TIME)):
            # first scan
            MY_DB['facebook'] = get_followers_facebook(accounts['facebook'])
            MY_DB['instagram'] = get_followers_instagram(accounts['instagram'])
            MY_DB['twitter'] = get_followers_twitter(ACCESS_TOKEN, accounts['twitter'])
            MY_DB['spotify'] = get_followers_spotify(accounts['spotify'])
            MY_DB['youtube'] = get_followers_youtube(YOUR_API_KEY, accounts['youtube'])
            MY_DB['last_date'] = now
        # Print message
        msg = f"🕸 {hbold(accounts['music_group_name'] + ' stats')} 🕸"
        msg += f"\nFacebook: {hbold(MY_DB['facebook'])}" if MY_DB['facebook'] else ''
        msg += f"\nInstagram: {hbold(MY_DB['instagram'])}" if MY_DB['instagram'] else ''
        msg += f"\nTwitter: {hbold(MY_DB['twitter'])}" if MY_DB['twitter'] else ''
        msg += f"\nSpotify: {hbold(MY_DB['spotify'])}" if MY_DB['spotify'] else ''
        msg += f"\nYoutube: {hbold(MY_DB['youtube'])}" if MY_DB['youtube'] else ''
        msg += f"\nUpdated: {MY_DB['last_date'].strftime('%Y-%m-%d %H:%M:%S')}" if MY_DB['last_date'] else ''
        logging.info(msg)
        await message.answer(msg, parse_mode='html')
    else:
        logging.warning('NOT ALLOWED')
        send_message(f'NOT ALLOWED: {message}')


@dp.message_handler(commands=['playlist'])
@restricted
async def search_playlist(message: types.Message, allowed):
    """
    This handler will be called when user sends `/playlist` command
    """
    if allowed:
        arguments = message.get_args()
        if arguments:
            query = arguments
        else:
            await message.answer('usage: /playlist TEXT TO SEARCH')
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
    else:
        logging.warning('NOT ALLOWED')
        send_message(f'NOT ALLOWED: {message}')


@dp.message_handler(commands=['random'])
@dp.message_handler(regexp='(random|frase|phrase|lletra|letra|lyric|aleatori)')
@restricted
async def random_song_phrase(message: types.Message, allowed):
    """
    Get all songs from 'lyrics' folder, choose a random one,
    extract the lyrics, parse it and return a random phrase.
    """
    all_songs = listdir(path.join(path.dirname(path.abspath(__file__)), 'lyrics'))
    random_song = choice(all_songs)

    with open(path.join(path.dirname(path.abspath(__file__)), 'lyrics', random_song), 'r') as f:
        phrases = f.readlines()
    phrases = list(set(phrases))  # delete duplicated lines
    phrases = [x for x in phrases if x and x != '\n']  # delete empty lines

    random_phrase = choice(phrases)
    random_phrase = random_phrase[:-1]  # delete last \n
    random_phrase = random_phrase[:-1] if random_phrase[-1] in [',', ':', ';'] else random_phrase

    msg = f"{random_phrase} \n🎵 {hitalic(accounts['music_group_name'] + ' - ' + random_song)} 🎵"
    logging.info(msg)
    await message.answer(msg, parse_mode='html')


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=False)
