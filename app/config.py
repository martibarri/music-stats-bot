import logging
from os import getenv
from pathlib import Path

from dotenv import load_dotenv

# Load environment variables
load_dotenv()


class Settings:

    # config variables
    FILENAME_LOG = getenv("FILENAME_LOG")
    FILENAME_DB = getenv("FILENAME_DB", "sqlite3.db")

    # create logs and data dir
    base_dir = Path(__file__).parent.parent
    DIR_LOG = base_dir / "logs"
    DIR_LOG.mkdir(parents=True, exist_ok=True)
    DIR_DATA = base_dir / "data"
    DIR_DATA.mkdir(parents=True, exist_ok=True)
    # define log and db filepath
    FILEPATH_LOG = DIR_LOG / FILENAME_LOG if FILENAME_LOG else None
    FILEPATH_DB = DIR_DATA / FILENAME_DB

    # Telegram
    API_TOKEN = getenv("API_TOKEN")
    MY_CHATID = int(getenv("MY_CHATID"))
    GROUP_CHATID = int(getenv("GROUP_CHATID"))
    try:
        ALLOW_LIST_CHATIDS = list(map(int, getenv("ALLOW_LIST_CHATIDS").split(",")))
    except Exception:
        ALLOW_LIST_CHATIDS = []
        logging.exception("ALLOW_LIST_CHATIDS error")

    # social
    SOCIAL_UPDATE_TIME = float(getenv("SOCIAL_UPDATE_TIME", 12))  # in hours
    # Set the name of public accounts
    accounts = {
        "music_group_name": "Sinergia",
        "facebook": "sinergiareggae",
        "instagram": "sinergiareggae",
        "twitter": "sinergiareggae",
        "spotify": "6i0i8gXIR3RQRnfWvRWrPa",
        "youtube": "UCsR3pSI6iRNlxyFkqmJ1tGg",
    }
    # Twitter
    ACCESS_TOKEN = getenv("ACCESS_TOKEN")
    # Youtube
    YOUR_API_KEY = getenv("YOUR_API_KEY")
