import logging
from datetime import datetime
from typing import List

from sqlmodel import Session, select

from db import engine
from models import Social, User


def get_last_social() -> Social:
    with Session(engine) as session:
        statement = select(Social).order_by(Social.id.desc()).limit(1)
        result = session.exec(statement).one_or_none()
    logging.info(f"SELECT social row: {result}")
    return result


def create_social(fb: int, ig: int, tw: int, sp: int, yt: int):
    dt_now = datetime.now().strftime("%Y%m%d_%H%M%S")
    logging.info(f"INSERT social row ({dt_now},{fb},{ig},{tw},{sp},{yt})")
    social_row = Social(dt=dt_now, fb=fb, ig=ig, tw=tw, sp=sp, yt=yt)
    with Session(engine) as session:
        session.add(social_row)
        session.commit()


def create_user(telegram_id: int, username: str = None, first_name: str = None, last_name: str = None):
    logging.info(f"INSERT user: {first_name}")
    user_row = User(telegram_id=telegram_id, username=username, first_name=first_name, last_name=last_name)
    with Session(engine) as session:
        session.add(user_row)
        session.commit()


def get_user(telegram_id: int) -> User:
    with Session(engine) as session:
        statement = select(User).where(User.telegram_id == telegram_id)
        result = session.exec(statement).one_or_none()
    logging.info(f"SELECT user: {result}")
    return result


def get_all_users() -> List[User]:
    with Session(engine) as session:
        statement = select(User)
        result = session.exec(statement).fetchall()
    logging.info(f"SELECT all users: {result}")
    return result
