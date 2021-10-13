import logging
import urllib

import requests
from config import Settings


def restricted(func):
    def func_wrapper(f):
        logging.info(f)
        chat_id = f["chat"]["id"]
        if chat_id in Settings.ALLOW_LIST_CHATIDS:
            return func(f, True)
        else:
            return func(f, False)
    return func_wrapper


def send_message(msg, api_token, my_chatid):
    parsedmsg = urllib.parse.quote_plus(msg)
    requests.get(f"https://api.telegram.org/bot{api_token}/sendMessage?chat_id={my_chatid}&text={parsedmsg}")
