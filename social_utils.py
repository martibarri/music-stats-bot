import requests
import json

from bs4 import BeautifulSoup


def get_followers_twitter(ACCESS_TOKEN, account_name):
    headers = {'authorization': f'Bearer {ACCESS_TOKEN}'}
    resp = requests.get(f'https://api.twitter.com/1.1/users/show.json?screen_name={account_name}', headers=headers)
    resp_json = json.loads(resp.text)
    followers = resp_json['followers_count']
    return followers


def get_followers_insta(account_name):
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
    following = text[2]
    if following[-1] == 'K':
        following = int(float(following[:-1].encode('UTF-8')) * 1000)
    else:
        following = int(float(following.encode('UTF-8')))
    return followers


def get_followers_facebook(account_name):
    html = requests.get(f'https://www.facebook.com/{account_name}/')
    soup = BeautifulSoup(html.text, 'html.parser')
    data = soup.find_all('meta', attrs={'name': 'description'})
    text = data[0].get('content').split()
    followers = text[2]
    return followers
