import logging
import sqlite3
from datetime import datetime

from config import Settings


class SocialRow:
    def __init__(self, row: tuple) -> None:
        try:
            self.id = row[0]
            self.dt = datetime.strptime(row[1], "%Y%m%d_%H%M%S")
            self.fb = row[2]
            self.ig = row[3]
            self.tw = row[4]
            self.sp = row[5]
            self.yt = row[6]
        except Exception:
            self.id = None
            self.dt = None
            self.fb = None
            self.ig = None
            self.tw = None
            self.sp = None
            self.yt = None

    def __repr__(self):
        return f"<SocialRow {dict(self.__dict__.items())}>"

    def __str__(self):
        return f"<SocialRow {dict(self.__dict__.items())}>"


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
    con.commit()
    con.close()


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
