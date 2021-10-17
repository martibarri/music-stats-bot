import logging
from datetime import datetime, timedelta
from pathlib import Path
from secrets import choice

from aiogram import Bot, Dispatcher, executor, types
from aiogram.utils.markdown import hbold, hitalic

from config import Settings
from utils.bot_utils import restricted, send_message
from utils.db_utils import db_init, db_social_insert, db_social_read_last
from utils.social_utils import print_social, social_query
from utils.spotify_utils import formatted_playlist, pretty_playlist, search_spotify

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    filename=Settings.FILEPATH_LOG,
    format="%(asctime)s.%(msecs)03d\t%(levelname)s\t%(name)s\t%(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)


# Initialize bot and dispatcher
bot = Bot(token=Settings.API_TOKEN)
dp = Dispatcher(bot)


@dp.message_handler(regexp="(xarx|social|xs|seguidor|follow|subscri|informaci|stats)")
@restricted
async def info_xxss(message: types.Message, allowed):
    if allowed:
        now = datetime.now()
        last_row = db_social_read_last()
        try:
            if now > last_row.dt + timedelta(hours=Settings.SOCIAL_UPDATE_TIME):
                logging.info("Update values...")
                update = True
            else:
                logging.info(
                    f"Cached values ({(now - last_row.dt).seconds}/{int(Settings.SOCIAL_UPDATE_TIME*3600)} seconds)"
                )
                update = False
        except TypeError:
            logging.warning("First scan")
            update = True
        if update:
            new_data = social_query()
            db_social_insert(*new_data)
            last_row = db_social_read_last()
        msg = print_social(last_row)
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
                await message.answer(
                    p, parse_mode="html", disable_web_page_preview=True
                )
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
    path_lyrics = Settings.base_dir / "app" / "lyrics"
    all_songs = list(map(lambda x: x.name, path_lyrics.iterdir()))
    random_song = choice(all_songs)

    with open(path_lyrics / random_song, "r") as f:
        phrases = f.readlines()
    phrases = list(set(phrases))  # delete duplicated lines
    phrases = [x for x in phrases if x and x != "\n"]  # delete empty lines

    random_phrase = choice(phrases)
    random_phrase = random_phrase[:-1]  # delete last \n
    random_phrase = (
        random_phrase[:-1] if random_phrase[-1] in [",", ":", ";"] else random_phrase
    )

    msg = f"{random_phrase} \n🎵 {hitalic(Settings.accounts['music_group_name'] + ' - ' + random_song)} 🎵"
    logging.info(msg)
    await message.answer(msg, parse_mode="html")


if __name__ == "__main__":
    db_init()
    executor.start_polling(dp, skip_updates=False)
