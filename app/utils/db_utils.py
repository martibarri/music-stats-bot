import logging
import sqlite3
from datetime import datetime

from config import Settings
from utils.models import SocialRow, UserRow


def db_init():
    con = sqlite3.connect(Settings.FILEPATH_DB)
    cur = con.cursor()
    try:
        cur.execute(
            """
            CREATE TABLE social (
                id INTEGER PRIMARY KEY,
                date TEXT,
                facebook INTEGER,
                instagram INTEGER,
                twitter INTEGER,
                spotify INTEGER,
                youtube INTEGER
            )
            """
        )
        logging.info("CREATE TABLE social")
    except sqlite3.OperationalError:
        logging.info("table 'social' already exists")
    try:
        cur.execute(
            """
            CREATE TABLE users (
                id INTEGER PRIMARY KEY,
                telegram_id INTEGER,
                username TEXT,
                first_name TEXT,
                last_name TEXT
            )
            """
        )
        logging.info("CREATE TABLE users")
    except sqlite3.OperationalError:
        logging.info("table 'users' already exists")
    con.commit()
    con.close()


def db_users_insert(telegram_id: int, username: str = None, first_name: str = None, last_name: str = None):
    con = sqlite3.connect(Settings.FILEPATH_DB)
    cur = con.cursor()
    cur.execute(
        f"""
        INSERT INTO users (telegram_id,username,first_name,last_name)
        VALUES (?, ?, ?, ?)
        """,
        (telegram_id, username, first_name, last_name),
    )
    logging.info(f"INSERT ({telegram_id},{username},{first_name},{last_name})")
    con.commit()
    con.close()


def db_users_get_by_id(telegram_id: int):
    logging.info(f"SELECT {telegram_id}")
    con = sqlite3.connect(Settings.FILEPATH_DB)
    cur = con.cursor()
    row = cur.execute("SELECT * FROM users WHERE telegram_id = ?", (telegram_id,)).fetchone()
    con.close()
    try:
        user_row = UserRow(row)
        logging.info(user_row)
    except Exception():
        logging.warning("User not found")
        user_row = None
    return user_row


def db_users_get_all():
    logging.info(f"SELECT all users")
    con = sqlite3.connect(Settings.FILEPATH_DB)
    cur = con.cursor()
    rows = cur.execute("SELECT * FROM users").fetchall()
    con.close()
    try:
        users = list(map(lambda x: UserRow(x), rows))
    except Exception:
        logging.exception("db_users_get_all")
        users = []
    logging.info(users)
    return users


def db_social_insert(fb: int, ig: int, tw: int, sp: int, yt: int):
    con = sqlite3.connect(Settings.FILEPATH_DB)
    cur = con.cursor()
    dt = datetime.now().strftime("%Y%m%d_%H%M%S")
    cur.execute(
        f"""
        INSERT INTO social (date,facebook,instagram,twitter,spotify,youtube)
        VALUES (?, ?, ?, ?, ?, ?)
        """,
        (dt, fb, ig, tw, sp, yt),
    )
    logging.info(f"INSERT ({dt},{fb},{ig},{tw},{sp},{yt})")
    con.commit()
    con.close()


def db_social_read_last():
    con = sqlite3.connect(Settings.FILEPATH_DB)
    cur = con.cursor()
    row = cur.execute("SELECT * FROM social ORDER BY id DESC LIMIT 1").fetchone()
    con.close()
    try:
        social_row = SocialRow(row)
    except TypeError:
        social_row = None
    logging.info(f"SELECT {social_row}")
    return social_row
