import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

client_id = 'xxxx'
client_secret = 'xxxx'
client_credentials_manager = spotipy.oauth2.SpotifyClientCredentials(client_id, client_secret)

spotify = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

name = 'rihanna'
result = spotify.search(q='artist:' + name, type='artist')
print(result)