import logging
import urllib

import requests
from config import Settings
from utils.db_utils import db_users_get_all


def restricted(func):
    def func_wrapper(f):
        logging.info(f)
        decision = f.chat.id in Settings.ALLOW_LIST_CHATIDS
        return func(f, decision)

    return func_wrapper


def restricted_group(func):
    def func_wrapper(f):
        logging.info(f)
        decision = (
            f.chat.id in Settings.ALLOW_LIST_CHATIDS
            and f.chat.type == "group"
            and f.chat.id == Settings.GROUP_CHATID
            and not f.from_user.is_bot
        )
        return func(f, decision)

    return func_wrapper


def restricted_member(func):
    def func_wrapper(f):
        logging.info(f)
        users_id = list(map(lambda u: u.telegram_id, db_users_get_all()))
        decision = f.from_user.id in users_id
        return func(f, decision)

    return func_wrapper


def restricted_admin(func):
    def func_wrapper(f):
        logging.info(f)
        decision = f.from_user.id == Settings.MY_CHATID
        return func(f, decision)

    return func_wrapper


def send_message(msg, api_token, my_chatid):
    parsedmsg = urllib.parse.quote_plus(msg)
    requests.get(f"https://api.telegram.org/bot{api_token}/sendMessage?chat_id={my_chatid}&text={parsedmsg}")


def send_admin_message(msg):
    send_message(msg, Settings.API_TOKEN, Settings.MY_CHATID)
