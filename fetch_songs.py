import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from schema import Artist, Album
from typing import List

client_id = 'xxxx'
client_secret = 'xxxx'
client_credentials_manager = spotipy.oauth2.SpotifyClientCredentials(
    client_id, client_secret)

spotify = spotipy.Spotify(
    client_credentials_manager=client_credentials_manager)


def main():
    """
    DynamoDB投入済みartistsの関連Artistの最新Albumを返す
    """
    # favorite_artists:List[Artist] = fetch_favorite_artist()
    favorite_artists = [
        Artist(
            name="",
            url="",
            spotify_uri="spotify:artist:19ojIp8CiO4yOQlvzVJEGS",
            image_url=""
        )
    ]
    new_artists: List[Artist] = []
    for artist in favorite_artists:
        new_artists += fetch_related_artists(artist.spotify_uri)
    new_albums: List[Album] = []
    for artist in new_artists:
        albums = fetch_albums(artist.spotify_uri)
        if albums:
            new_albums.append(albums[0])
    for index in range(len(new_artists)):
        print(new_artists[index])
        print(new_albums[index])


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


def fetch_albums(artist_uri: str) -> List[Album]:
    """
    入力artist_uriの全album情報を解禁日新しい順に返す
    """
    albums = spotify.artist_albums(artist_uri)["items"]
    albums = sorted(albums, key=lambda x: -
                    int(x["release_date"].replace("-", "")))
    for i in range(len(albums)):
        albums[i] = Album(
            name=albums[i]["name"],
            url=albums[i]["href"],
            image_url=albums[i]["images"][0]["url"]
        )
    return albums


print(main())
