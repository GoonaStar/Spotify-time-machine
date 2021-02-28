import requests
from bs4 import BeautifulSoup
import spotipy
from spotipy.oauth2 import SpotifyOAuth
import os
from pprint import pprint

answer_choice = input("Which year do you want to travel to? (YYYY-MM-DD)")

url="https://www.billboard.com/charts/hot-100/"
response = requests.get(f"{url}{answer_choice}")
billboard_page = response.text

soup = BeautifulSoup(billboard_page, "html.parser")
song_names_span = soup.findAll("span", class_="chart-element__information__song")

song_names = [song_name.getText() for song_name in song_names_span[:5]]

scope = "playlist-modify-private"

sp = spotipy.Spotify(auth_manager=SpotifyOAuth(
    scope=scope,
    client_id=os.environ.get("SPOTIPY_CLIENT_ID"),
    client_secret=os.environ.get("SPOTIPY_CLIENT_SECRET"),
    redirect_uri=os.environ.get("SPOTIPY_REDIRECT_URI"),
    show_dialog=True,
    cache_path="token.txt"))

year = answer_choice.split("-")[0]
user_id = sp.current_user()["id"]

list_songs_uri = []

for song in song_names:
    results = sp.search(q=f"track: {song} year: {year}", limit=1, type='track')
    try:
        song_uri = results["tracks"]["items"][0]["uri"]
        list_songs_uri.append(song_uri)
    except IndexError:
        print(f"{song} does not exist here")

playlist = sp.user_playlist_create(user=user_id, name=f"{answer_choice} Billboard 100",public=False)
sp.playlist_add_items(playlist["id"], items=list_songs_uri)
print(playlist)




