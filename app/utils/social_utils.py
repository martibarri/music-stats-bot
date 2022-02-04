import json
import logging
from datetime import datetime

import requests
import spotipy
from aiogram.utils.markdown import hbold
from bs4 import BeautifulSoup
from config import Settings
from models import Social, SocialMap


def get_followers_twitter(ACCESS_TOKEN, account_name):
    try:
        headers = {"authorization": f"Bearer {ACCESS_TOKEN}"}
        url = f"https://api.twitter.com/1.1/users/show.json?screen_name={account_name}"
        resp = requests.get(url, headers=headers)
        resp_json = json.loads(resp.text)
        followers = resp_json["followers_count"]
        return int(followers)
    except Exception:
        logging.exception("Error getting twitter followers")
        return None


def get_followers_instagram(account_name):
    try:
        html = requests.get(f"https://www.instagram.com/{account_name}/")
        soup = BeautifulSoup(html.text, "html.parser")
        data = soup.find_all("meta", attrs={"property": "og:description"})
        text = data[0].get("content").split()
        # user = f"{text[-3]} {text[-2]} {text[-1]}"
        followers = text[0]
        if followers[-1] == "K":
            followers = int(float(followers[:-1].encode("UTF-8")) * 1000)
        else:
            followers = int(float(followers.encode("UTF-8")))
        return int(followers)
    except Exception:
        logging.exception("Error getting instagram followers")
        return None


def get_followers_facebook(account_name):
    try:
        html = requests.get(f"https://www.facebook.com/{account_name}/")
        soup = BeautifulSoup(html.text, "html.parser")
        data = soup.find_all("meta", attrs={"name": "description"})
        text = data[0].get("content").split()
        followers = text[2]
        return int(followers)
    except Exception:
        logging.exception("Error getting facebook followers")
        return None


def get_followers_spotify(artist_id):
    try:
        client_credentials_manager = spotipy.oauth2.SpotifyClientCredentials()
        sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)
        urn = f"spotify:artist:{artist_id}"
        artist = sp.artist(urn)
        followers = artist.get("followers", {}).get("total")
        return int(followers)
    except Exception:
        logging.exception("Error getting spotify followers")
        return None


def get_followers_youtube(YOUR_API_KEY, channel_id):
    try:
        url = f"https://www.googleapis.com/youtube/v3/channels?part=statistics&id={channel_id}&key={YOUR_API_KEY}"
        response = requests.get(url)
        resp_json = json.loads(response.text)
        subscribers = resp_json["items"][0]["statistics"]["subscriberCount"]
        return int(subscribers)
    except Exception:
        logging.exception("Error getting youtube followers")
        return None


def social_query() -> tuple:
    fb = get_followers_facebook(Settings.accounts["facebook"])
    ig = get_followers_instagram(Settings.accounts["instagram"])
    tw = get_followers_twitter(Settings.ACCESS_TOKEN, Settings.accounts["twitter"])
    sp = get_followers_spotify(Settings.accounts["spotify"])
    yt = get_followers_youtube(Settings.YOUR_API_KEY, Settings.accounts["youtube"])
    return (fb, ig, tw, sp, yt)


def social_diff(a, b):
    try:
        diff = int(b) - int(a)
        if diff != 0:
            return f"({diff:+})"
        else:
            return
    except Exception:
        return


def build_social_msg(slug, row: dict, prow: dict):
    msg = ""
    name = SocialMap.map.get(slug)
    if name:
        row_value = row.get(slug)
        prow_value = prow.get(slug)
        if row_value:
            msg += f"\n{name}: {hbold(row_value)}"
            diff = social_diff(prow_value, row_value)
            if diff:
                msg += f" {diff}"
    return msg


def print_social(row: Social, prow: Social) -> str:
    # Print message
    msg = f"🕸 {hbold(Settings.accounts['music_group_name'] + ' stats')} 🕸"
    try:
        row_dict = row.dict()
    except Exception:
        row_dict = {}
    try:
        prow_dict = prow.dict()
    except Exception:
        prow_dict = {}
    for i, _ in row:
        msg += build_social_msg(i, row_dict, prow_dict)
    msg += f"\nUpdated: {datetime.strptime(row.dt, '%Y%m%d_%H%M%S').strftime('%Y-%m-%d %H:%M:%S')}" if row.dt else ""
    return msg
