import spotipy

from aiogram.utils.markdown import hbold


def formatted_playlist(playlist):
    followers = playlist['followers']['total']
    tracks = playlist['tracks']['total']
    name = playlist['name']
    owner = playlist['owner']['display_name']
    url = playlist['external_urls']['spotify']
    return (followers, tracks, name, owner, url)


def pretty_playlist(f):
    pretty = f"{hbold('Followers')}: {f[0]}\n{hbold('Tracks')}: {f[1]}\n{hbold('Name')}: {f[2]}\n{hbold('Owner')}: {f[3]}\n{f[4]}"
    return pretty


def search_spotify(search_type, query, limit_search, market):

    client_credentials_manager = spotipy.oauth2.SpotifyClientCredentials()
    sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

    if search_type == 'playlist':
        # Search playlists
        response = sp.search(query, type=search_type, limit=limit_search)
        resp_playlists = response['playlists']['items']
        playlists_id = []
        for p in resp_playlists:
            playlists_id.append(p['id'])
        # Get playlist objects
        playlists = []
        for p_id in playlists_id:
            # https://developer.spotify.com/documentation/web-api/reference/playlists/get-playlist/
            fields = 'name,followers,external_urls,tracks,owner'
            playlist = sp.playlist(playlist_id=p_id, market=market, fields=fields)
            playlists.append(playlist)

        # Sort playlists by followers
        playlists = sorted(playlists, key=lambda x: x['followers']['total'], reverse=True)

        return playlists
