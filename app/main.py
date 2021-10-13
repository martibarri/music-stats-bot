import logging
from datetime import datetime, timedelta
from os import listdir, path
from pathlib import Path
from secrets import choice

from aiogram import Bot, Dispatcher, executor, types
from aiogram.utils.markdown import hbold, hitalic

from config import Settings
from utils.bot_utils import restricted, send_message
from utils.social_utils import (get_followers_facebook,
                                get_followers_instagram, get_followers_spotify,
                                get_followers_twitter, get_followers_youtube)
from utils.spotify_utils import (formatted_playlist, pretty_playlist,
                                 search_spotify)
from utils.sqlite_utils import *

# Configure logging
if Settings.LOGGING_FILE:
    Path(Settings.LOGGING_PATH).mkdir(parents=True, exist_ok=True)
    logging.basicConfig(
        level=logging.INFO,
        filename=Path(Settings.LOGGING_PATH) / Path(Settings.LOGGING_FILE),
        filemode="a",
        format="%(asctime)s.%(msecs)03d\t%(levelname)s\t%(name)s\t%(message)s",
        datefmt="%Y-%m-%d %H:%M:%S"
    )
else:
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s.%(msecs)03d\t%(levelname)s\t%(name)s\t%(message)s",
        datefmt="%Y-%m-%d %H:%M:%S"
    )


# Initialize bot and dispatcher
bot = Bot(token=Settings.API_TOKEN)
dp = Dispatcher(bot)


@dp.message_handler(regexp="(xarx|social|xs|seguidor|follow|subscri|informaci|stats)")
@restricted
async def info_xxss(message: types.Message, allowed):
    if allowed:
        now = datetime.utcnow()
        # First scan or rescan + update values
        if (not Settings.MY_DB["last_date"]) or (now > Settings.MY_DB["last_date"] + timedelta(hours=Settings.SOCIAL_UPDATE_TIME)):
            # first scan
            Settings.MY_DB["facebook"] = get_followers_facebook(Settings.accounts["facebook"])
            Settings.MY_DB["instagram"] = get_followers_instagram(Settings.accounts["instagram"])
            Settings.MY_DB["twitter"] = get_followers_twitter(Settings.ACCESS_TOKEN, Settings.accounts["twitter"])
            Settings.MY_DB["spotify"] = get_followers_spotify(Settings.accounts["spotify"])
            Settings.MY_DB["youtube"] = get_followers_youtube(Settings.YOUR_API_KEY, Settings.accounts["youtube"])
            Settings.MY_DB["last_date"] = now
        # Print message
        msg = f"🕸 {hbold(Settings.accounts['music_group_name'] + ' stats')} 🕸"
        msg += f"\nFacebook: {hbold(Settings.MY_DB['facebook'])}" if Settings.MY_DB["facebook"] else ""
        msg += f"\nInstagram: {hbold(Settings.MY_DB['instagram'])}" if Settings.MY_DB["instagram"] else ""
        msg += f"\nTwitter: {hbold(Settings.MY_DB['twitter'])}" if Settings.MY_DB["twitter"] else ""
        msg += f"\nSpotify: {hbold(Settings.MY_DB['spotify'])}" if Settings.MY_DB["spotify"] else ""
        msg += f"\nYoutube: {hbold(Settings.MY_DB['youtube'])}" if Settings.MY_DB["youtube"] else ""
        msg += f"\nUpdated: {Settings.MY_DB['last_date'].strftime('%Y-%m-%d %H:%M:%S')}" if Settings.MY_DB["last_date"] else ""
        logging.info(msg)
        await message.answer(msg, parse_mode="html")
    else:
        logging.warning("NOT ALLOWED")
        send_message(f"NOT ALLOWED: {message}", Settings.API_TOKEN, Settings.MY_CHATID)


@dp.message_handler(commands=["playlist"])
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
            await message.answer("usage: /playlist TEXT TO SEARCH")
            return

        ##########################
        query += " NOT reggaeton"
        limit_search = 20
        minim_followers = 200
        search_type = "playlist"
        market = "ES"
        ##########################

        logging.info(f"query: {query} by user {types.User.get_current()}")

        playlists = search_spotify(search_type, query, limit_search, market)

        pretty_playlists = []
        for p in playlists:
            if p["followers"]["total"] > minim_followers:
                f = formatted_playlist(p)
                logging.info(f)
                p = pretty_playlist(f)
                await message.answer(p, parse_mode="html", disable_web_page_preview=True)
                pretty_playlists.append(p)

        search_result = f"{len(pretty_playlists)} relevant results of {len(playlists)} response results"
        logging.info(search_result)
        await message.answer(search_result)
    else:
        logging.warning("NOT ALLOWED")
        send_message(f"NOT ALLOWED: {message}", Settings.API_TOKEN, Settings.MY_CHATID)


@dp.message_handler(commands=["random"])
@dp.message_handler(regexp="(random|frase|phrase|lletra|letra|lyric|aleatori)")
@restricted
async def random_song_phrase(message: types.Message, allowed):
    """
    Get all songs from "lyrics" folder, choose a random one,
    extract the lyrics, parse it and return a random phrase.
    """
    all_songs = listdir(path.join(path.dirname(path.abspath(__file__)), "lyrics"))
    random_song = choice(all_songs)

    with open(path.join(path.dirname(path.abspath(__file__)), "lyrics", random_song), "r") as f:
        phrases = f.readlines()
    phrases = list(set(phrases))  # delete duplicated lines
    phrases = [x for x in phrases if x and x != "\n"]  # delete empty lines

    random_phrase = choice(phrases)
    random_phrase = random_phrase[:-1]  # delete last \n
    random_phrase = random_phrase[:-1] if random_phrase[-1] in [",", ":", ";"] else random_phrase

    msg = f"{random_phrase} \n🎵 {hitalic(Settings.accounts['music_group_name'] + ' - ' + random_song)} 🎵"
    logging.info(msg)
    await message.answer(msg, parse_mode="html")


if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=False)
