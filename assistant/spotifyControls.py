import time

import spotipy
import os
from dotenv import load_dotenv
from assistant.basic import match_substring
import threading
from pprint import pprint

load_dotenv()
clientSecret = os.getenv("SPOTIPY_SECRET")
clientID = os.getenv("SPOTIPY_CLIENT_ID")
redirectURI = os.getenv("SPORIFY_REDIRECT_URI")

scope = 'user-library-read user-modify-playback-state user-read-playback-state user-read-playback-position' \
        ' user-read-email user-read-private user-read-recently-played' \
        ' streaming playlist-modify-private playlist-read-private playlist-modify-public user-library-modify '

oauth = spotipy.SpotifyOAuth(client_id=clientID, client_secret=clientSecret, redirect_uri=redirectURI, scope=scope)
token_dict = oauth.get_access_token()
token = token_dict['access_token']
refresh_token = token_dict['refresh_token']
sp = spotipy.Spotify(auth= token)

device = sp.devices()['devices'][0]


def get_playlists_by_keyword(keyword):
    print(f"Searching for playlist matching {keyword}")
    results = []
    try:
        while True:
            for offset in range(0, 100, 50):
                for item in sp.current_user_playlists(limit=50, offset=offset)['items']:
                    if match_substring(keyword, item['name']):
                        results.append(item)
            break
    except:
        return results
    return results


def play(keyword):
    if not keyword:
        resume()
        return
    try:
        playlist = get_playlists_by_keyword(keyword)[0]
        playlist_uri = get_playlist_uri(playlist)
        playlist_name = get_playlist_name(playlist)
        sp.start_playback(device_id=device.get('id'), context_uri=playlist_uri)
        print(f"Now Playing: {playlist_name}")
    except:
        print(f"Playlist with keyword '{keyword}' not found in your library\nsearching Spotify for public Playlists")
        try:
            playlist = search_playlist(keyword)
            if not playlist:
                raise Exception
            else:
                print(f"Now playing: {playlist['name']} By: {get_user_name(get_playlist_owner(playlist))}")
                sp.start_playback(device_id=device.get('id'), context_uri=playlist['uri'])
        except:
            print(f"Could not find anything for {keyword}")


def next_track():
    sp.next_track(device_id=device['id'])


def previous_track():
    sp.previous_track(device_id=device['id'])


def can_pause():
    try:
        return sp.currently_playing().get('actions').get('disallows').get('pausing')
    except:
        return False


def pause():
    if not can_pause():
        sp.pause_playback(device_id=device.get('id'))


def resume():
    if can_pause():
        sp.start_playback(device_id=device.get('id'))


def shuffle():
    sp.shuffle(True, device_id=device['id'])


def volume_up(amount: int = 10):
    global device
    device = sp.current_playback().get('device')
    current_vol = int(device['volume_percent'])
    if current_vol < 100:
        target_vol = amount + current_vol
        if target_vol > 100:
            target_vol = 100
        sp.volume(target_vol, device_id=device.get('id'))


def volume_down(amount: int = 10):
    global device
    device = sp.current_playback().get('device')
    current_vol = int(device['volume_percent'])
    if current_vol > 0:
        target_vol = current_vol - amount
        if target_vol < 0:
            target_vol = 0
        sp.volume(target_vol, device_id=device.get('id'))


def volume_set(amount: int):
    global device
    device = sp.current_playback().get('device')
    if amount < 0:
        sp.volume(0, device_id=device.get('id'))
        print("Volume cannot go lower than 0%")
    elif amount > 100:
        sp.volume(100, device_id=device.get('id'))
        print("Volume cannot go higher than 100%")
    else:
        sp.volume(amount, device_id=device.get('id'))
        print(f"Volume set to {amount}%")


def restart():
    global device
    device = sp.current_playback().get('device')
    sp.seek_track(position_ms=0, device_id=device.get('id'))


def now_playing():
    try:
        useful_info = ["artists", "name"]
        track = sp.currently_playing().get('item')
        return {key: track[key] for key in useful_info}
    except AttributeError:
        return "No song currently playing"


def search_song(keyword: str):
    song = sp.search(q=keyword, limit=1)['tracks']['items'][0]
    return song


def search_playlist(keyword: str):
    playlist = sp.search(keyword, type="playlist", limit=1)['playlists']['items'][0]
    return playlist


def get_user_name(user):
    return user.get("display_name")


def get_playlist_owner(playlist):
    return playlist.get("owner")


def get_playlist_uri(playlist):
    return playlist.get("uri")


def get_playlist_name(playlist):
    return playlist.get("name")


def refresh_access_token():
    time.sleep(600)
    global token_dict, refresh_token,token,sp
    token_dict = oauth.refresh_access_token(refresh_token)
    token_dict = oauth.get_access_token()
    token = token_dict['access_token']
    refresh_token = token_dict['refresh_token']
    sp = spotipy.Spotify(auth=token)


t1 = threading.Thread(target=refresh_access_token)
t1.start()