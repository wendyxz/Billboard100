import requests
from bs4 import BeautifulSoup
import spotipy
import pprint
from spotipy.oauth2 import SpotifyOAuth
import config

URL = "https://www.billboard.com/charts/hot-100/"
date = input("Which year do you want to travel to? Type the date in this format YYYY-MM-DD:")
response = requests.get(URL + date)

soup = BeautifulSoup(response.text, "html.parser")

top_100_songs_tags = soup.find_all(name="h3", class_="c-title a-no-trucate a-font-primary-bold-s u-letter-spacing-0021 lrv-u-font-size-18@tablet lrv-u-font-size-16 u-line-height-125 u-line-height-normal@mobile-max a-truncate-ellipsis u-max-width-330 u-max-width-230@tablet-only", id="title-of-a-story")
top_100_songs = [song.text.strip() for song in top_100_songs_tags]

top_100_artists_tags = soup.find_all(name="span", class_="c-label a-no-trucate a-font-primary-s lrv-u-font-size-14@mobile-max u-line-height-normal@mobile-max u-letter-spacing-0021 lrv-u-display-block a-truncate-ellipsis-2line u-max-width-330 u-max-width-230@tablet-only")
top_100_artists = [artist.text.strip() for artist in top_100_artists_tags]

sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=config.SPOTIFY_CLIENT_ID, client_secret=config.SPOTIFY_CLIENT_SECRET,
                                               redirect_uri="http://example.com", scope="playlist-modify-private", cache_path="token.txt", show_dialog=True))
user_id = sp.current_user()["id"]

q_list = dict(zip(top_100_songs, top_100_artists))
song_uris = []
result = sp.search(q=f"track:{top_100_songs[0]} artist:{top_100_artists[0]}", type="track")

for song, artist in q_list.items():
    result = sp.search(q=f"{song} {artist}", type="track", limit=5)
    try:
        uri = result["tracks"]["items"][0]["uri"]
        song_uris.append(uri)
    except IndexError:
        print(f"{song} by {artist} doesn't exist in Spotify. Skipped...")

# pp = pprint.PrettyPrinter(indent=1)
playlist = sp.user_playlist_create(user=user_id, name=f"Billboard 100 {date}", public=False)
sp.playlist_add_items(playlist_id=playlist["id"], items=song_uris)

# print(sp.current_user_playlists(limit=50))




