# music-stats-bot
Telegram bot of my music group

# Initialization

1. Copy the sample environment file to a new '.env' and fill in the corresponding credentials

        cp .env.sample .env

2. Create a virtual environment

        mkvirtualenv --python=`which python3` music-stats-bot

3. Install requirements inside the new environment 

        pip install -r requirements.txt

4. Edit accounts name in `main.py`

    _sinergiareggae_ is just my music group

    `SOCIAL_UPDATE_TIME` can also be changed

5. Run project

        python main.py


# Functionalities

## Allowlist usage

`ALLOW_LIST_CHATIDS` is a comma-separated list of ChatIDs that are allowed to use the bot.

## Restricted usage notification

`CHATID` is the my personal Telegram chat ID, and is where security messages will be sent.

## Print social networks stats

if bot can read all messages with the assigned option `/setprivacy` of @BotFather, any of the following words will print the stats:

`regexp='(xarx|social|xs|seguidor|follow|subscri|informaci|stats)'`

## Search Spotify playlists

Usage: `/playlist KEYWORDS`

## Random Song Phrase

Function that choose a random phrase of the available songs of the `lyrics` folder.
