import spotipy
import os
from dotenv import load_dotenv
from assistant.basic import match_substring
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

sp = spotipy.Spotify(auth=token_dict['access_token'])

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


def play_playlist(keyword):
    try:
        playlist = get_playlists_by_keyword(keyword)[0]
        playlist_uri = playlist['uri']
        playlist_name = playlist['name']
        sp.start_playback(device_id=device.get('id'), context_uri=playlist_uri)
        print(f"Now Playing: {playlist_name}")
    except:
        print(f"Playlist with keyword '{keyword}' not found in your library")


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
    device =sp.current_playback().get('device')
    sp.seek_track(position_ms=0,device_id=device.get('id'))


def now_playing():
    return sp.currently_playing()
