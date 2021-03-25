import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from schema import Artist
from typing import List

client_id = 'xxxx'
client_secret = 'xxxx'
client_credentials_manager = spotipy.oauth2.SpotifyClientCredentials(
    client_id, client_secret)

spotify = spotipy.Spotify(
    client_credentials_manager=client_credentials_manager)


def fetch_related_artists(artist_uri: str) -> List[Artist]:
    """
    artists_uriを受け取って関連アーティスト情報をArtistにまとめて返す
    """
    response = spotify.artist_related_artists(
        'spotify:artist:19ojIp8CiO4yOQlvzVJEGS')
    related_artists: List[Artist] = []
    for artist in response["artists"]:
        artist_info = Artist(
            name=artist["name"],
            url=artist["external_urls"]["spotify"],
            spotify_uri=artist["uri"],
            # アーティスト画像はないこともあるので空を許す
            image_url=artist["images"][0]["url"] if artist["images"] else ""
        )
        related_artists.append(artist_info)
    return related_artists


def fetch_newest_album(artist_uri: str) -> str:
    """
    入力artist_uriの最新のalbumを返す
    """
    albums = spotify.artist_albums(artist_uri)
    print(albums)
    return None


print(fetch_newest_album("spotify:artist:19ojIp8CiO4yOQlvzVJEGS"))
