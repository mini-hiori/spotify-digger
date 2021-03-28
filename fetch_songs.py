from const import spotify,webhook_url

from schema import Album
from typing import List
from dynamodb import scan_dynamodb, put_dynamodb,delete_dynamodb
import random
import requests
import json
 

def main():
    """
    DynamoDB投入済みartistsの関連Artistの最新Albumを返す
    """
    favorite_artists: str = scan_dynamodb()
    new_artists: str = []
    for artist_uri in favorite_artists:
        candidates: List[str] = fetch_related_artists(artist_uri)
        new_artists += [i for i in candidates if i not in favorite_artists]
    # DynamoDB内のartistの関連artistのうち、まだDynamoDBにいない3人をdigる
    # あえてnew_artistsの重複排除はしない(重複したartistはピックアップ確率があがる？)
    target_artists: str = random.sample(new_artists,3)

    new_albums: List[Album] = []
    for artist_uri in target_artists:
        albums = fetch_albums(artist_uri)
        if albums:
            new_albums.append(albums[0])
    for artist in target_artists:
        put_dynamodb(artist)
    for index in range(len(new_albums)):
        print(new_albums[index])
        post_message = {
            "content": f"""
            Artist:{new_albums[index].artist_name}
            Album_name:{new_albums[index].album_name}
            Album_url:{new_albums[index].album_url}
            """,
            "embeds": [{
                    'description': new_albums[index].album_name,
                    'image': {
                        'url': new_albums[index].album_image_url
                    }
            }]
        }
        requests.post(webhook_url,json.dumps(post_message),headers={'Content-Type': 'application/json'})
    if len(favorite_artists) > 500:
        # DynamoDBに入れるアーティスト上限 とりあえず500人まで
        delete_target: List[str] = random.sample(new_artists,3)
        for uri in delete_target:
            delete_dynamodb(uri)



def fetch_related_artists(artist_uri: str) -> List[str]:
    """
    入力artists_uriの関連アーティストのuriを返す
    """
    response = spotify.artist_related_artists(artist_uri)
    related_artists: List[str] = []
    for artist in response["artists"]:
        related_artists.append(artist["uri"])
    return related_artists


def fetch_albums(artist_uri: str) -> List[Album]:
    """
    入力artist_uriの全album情報を解禁日新しい順に返す
    """
    albums = spotify.artist_albums(artist_uri)["items"]
    albums = sorted(albums, key=lambda x: -
                    int(x["release_date"].replace("-", "")))
    for i in range(len(albums)):
        artist_info = spotify.artist(artist_uri)
        albums[i] = Album(
            album_name=albums[i]["name"],
            album_url=albums[i]["external_urls"]["spotify"],
            album_image_url=albums[i]["images"][0]["url"],
            artist_uri=artist_uri,
            artist_name=artist_info["name"],
            artist_url=artist_info["external_urls"]["spotify"]
        )
    return albums


if __name__ == "__main__":
    main()
