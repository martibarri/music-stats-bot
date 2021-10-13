from os import getenv

from dotenv import load_dotenv

# Load environment variables
load_dotenv()


class Settings:
    # Secrets
    LOGGING_PATH = getenv("LOGGING_PATH", "logs")
    LOGGING_FILE = getenv("LOGGING_FILE")
    API_TOKEN = getenv("API_TOKEN")  # Telegram
    MY_CHATID = getenv("MY_CHATID")  # Telegram
    ACCESS_TOKEN = getenv("ACCESS_TOKEN")  # Twitter
    YOUR_API_KEY = getenv("YOUR_API_KEY")  # Youtube
    ALLOW_LIST_CHATIDS = list(map(int, getenv("ALLOW_LIST_CHATIDS").split(",")))  # Telegram
    DB_NAME = getenv("DB_NAME", "sqlite3.db")

    # config variables
    SOCIAL_UPDATE_TIME = 12  # in hours
    # Set the name of public accounts
    accounts = {
        "music_group_name": "Sinergia",
        "facebook": "sinergiareggae",
        "instagram": "sinergiareggae",
        "twitter": "sinergiareggae",
        "spotify": "6i0i8gXIR3RQRnfWvRWrPa",
        "youtube": "UCsR3pSI6iRNlxyFkqmJ1tGg",
    }

    MY_DB = {
        "last_date": None,
        "facebook": None,
        "instagram": None,
        "twitter": None,
        "spotify": None,
        "youtube": None,
    }
