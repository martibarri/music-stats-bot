import logging
from datetime import datetime, timedelta
from secrets import choice

from aiogram import Bot, Dispatcher, executor, types
from aiogram.utils.markdown import hitalic

import crud
from config import Settings
from db import create_db_and_tables
from utils.bot_utils import restricted, restricted_admin, restricted_group, send_admin_message
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
async def info_xxss(message: types.Message, allowed: bool):
    if allowed:
        now = datetime.now()
        last_row = crud.get_last_social()
        try:
            last_scan = datetime.strptime(last_row.dt, "%Y%m%d_%H%M%S")
            if now > last_scan + timedelta(hours=Settings.SOCIAL_UPDATE_TIME):
                logging.info("Update values...")
                update = True
            else:
                logging.info(
                    f"Cached values ({(now - last_scan).seconds}/{int(Settings.SOCIAL_UPDATE_TIME*3600)} seconds)"
                )
                update = False
        except (TypeError, AttributeError):
            logging.warning("First scan")
            update = True
        if update:
            new_data = social_query()
            crud.create_social(*new_data)
            last_row = crud.get_last_social()
        previous_row = crud.get_previous_social()
        msg = print_social(last_row, previous_row)
        logging.info(msg)
        await message.answer(msg, parse_mode="html")
    else:
        logging.warning("NOT ALLOWED")
        send_admin_message(f"NOT ALLOWED: {message}")


@dp.message_handler(commands=["playlist"])
@restricted
async def search_playlist(message: types.Message, allowed: bool):
    """
    This handler will be called when user sends `/playlist` command
    """
    if allowed:
        arguments = message.get_args()
        if arguments:
            query = str(arguments)
        else:
            await message.answer("usage: /playlist TEXT TO SEARCH")
            return

        ##########################
        query += " NOT reggaeton"
        limit_search = 20
        minim_followers = 100
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
        send_admin_message(f"NOT ALLOWED: {message}")


@dp.message_handler(commands=["random"])
@dp.message_handler(regexp="(random|frase|phrase|lletra|letra|lyric|aleatori)")
@restricted
async def random_song_phrase(message: types.Message, allowed: bool):
    """
    Get all songs from "lyrics" folder, choose a random one,
    extract the lyrics, parse it and return a random phrase.
    """
    if allowed:
        path_lyrics = Settings.base_dir / "app" / "lyrics"
        all_songs = list(map(lambda x: x.name, path_lyrics.iterdir()))
        random_song = choice(all_songs)

        with open(path_lyrics / random_song, "r") as f:
            phrases = f.readlines()
        phrases = list(set(phrases))  # delete duplicated lines
        phrases = [x for x in phrases if x and x != "\n"]  # delete empty lines

        random_phrase = choice(phrases)
        random_phrase = random_phrase[:-1]  # delete last \n
        random_phrase = random_phrase[:-1] if random_phrase[-1] in [",", ":", ";"] else random_phrase

        msg = f"{random_phrase} \n🎵 {hitalic(Settings.accounts['music_group_name'] + ' - ' + random_song)} 🎵"
        logging.info(msg)
        await message.answer(msg, parse_mode="html")
    else:
        logging.warning("NOT ALLOWED")
        send_admin_message(f"NOT ALLOWED: {message}")


@dp.message_handler(commands=["register"])
@restricted_group
async def user_register(message: types.Message, allowed: bool):
    if allowed:
        if not message.from_user.is_bot:
            user = crud.get_user(message.from_user.id)
            if user:
                await message.answer("User already registered")
            else:
                # register user
                crud.create_user(
                    telegram_id=message.from_user.id,
                    username=message.from_user.username,
                    first_name=message.from_user.first_name,
                    last_name=message.from_user.last_name,
                )
                user = crud.get_user(message.from_user.id)
                if user:
                    await message.answer("User successfully registered")
                else:
                    await message.answer(f"Some error registering user {message.from_user}")
    else:
        logging.warning("NOT ALLOWED")
        send_admin_message(f"NOT ALLOWED: {message}")


@dp.message_handler(commands=["users"])
@restricted_admin
async def list_users(message: types.Message, allowed: bool):
    if allowed:
        users = crud.get_all_users()
        await message.answer(users)
    else:
        logging.warning("NOT ALLOWED")
        send_admin_message(f"NOT ALLOWED: {message}")


@dp.message_handler(commands=["msg"])
@restricted
async def replay_msg(message: types.Message, allowed: bool):
    if allowed:
        await message.answer(message)
    else:
        logging.warning("NOT ALLOWED")
        send_admin_message(f"NOT ALLOWED: {message}")


@dp.message_handler(commands=["info_chat"])
@restricted
async def get_info_chat(message: types.Message, allowed: bool):
    if allowed:
        await message.answer("chat info sent!")
        send_admin_message(f"get_info_chat: {message.chat}")
    else:
        logging.warning("NOT ALLOWED")
        send_admin_message(f"NOT ALLOWED: {message}")


if __name__ == "__main__":
    create_db_and_tables()
    executor.start_polling(dp, skip_updates=False)
