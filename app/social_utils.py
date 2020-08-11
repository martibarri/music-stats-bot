import requests
import json

from bs4 import BeautifulSoup


def get_followers_twitter(ACCESS_TOKEN, account_name):
    try:
        headers = {'authorization': f'Bearer {ACCESS_TOKEN}'}
        resp = requests.get(f'https://api.twitter.com/1.1/users/show.json?screen_name={account_name}', headers=headers)
        resp_json = json.loads(resp.text)
        followers = resp_json['followers_count']
        return followers
    except Exception:
        return None


def get_followers_instagram(account_name):
    try:
        html = requests.get(f'https://www.instagram.com/{account_name}/')
        soup = BeautifulSoup(html.text, 'html.parser')
        data = soup.find_all('meta', attrs={'property': 'og:description'})
        text = data[0].get('content').split()
        # user = f'{text[-3]} {text[-2]} {text[-1]}'
        followers = text[0]
        if followers[-1] == 'K':
            followers = int(float(followers[:-1].encode('UTF-8')) * 1000)
        else:
            followers = int(float(followers.encode('UTF-8')))
        return followers
    except Exception:
        return None


def get_followers_facebook(account_name):
    try:
        html = requests.get(f'https://www.facebook.com/{account_name}/')
        soup = BeautifulSoup(html.text, 'html.parser')
        data = soup.find_all('meta', attrs={'name': 'description'})
        text = data[0].get('content').split()
        followers = text[2]
        return followers
    except Exception:
        return None


def get_followers_spotify(artist_id):
    try:
        html = requests.get(f'https://open.spotify.com/follow/1?uri=spotify:artist:{artist_id}&show-count=1')
        soup = BeautifulSoup(html.text, 'html.parser')
        data = soup.find_all('div', attrs={'class': 'count-num'})
        followers = data[0].getText()
        # new_followers = data[1].getText()
        return followers
    except Exception:
        return None


def get_followers_youtube(YOUR_API_KEY, channel_id):
    try:
        url = f'https://www.googleapis.com/youtube/v3/channels?part=statistics&id={channel_id}&key={YOUR_API_KEY}'
        response = requests.get(url)
        resp_json = json.loads(response.text)
        subscribers = resp_json['items'][0]['statistics']['subscriberCount']
        return subscribers
    except Exception:
        return None
