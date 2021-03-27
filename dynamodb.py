import boto3
import datetime
from typing import List
from const import spotify


def scan_dynamodb() -> List[str]:
    """
    DynamoDBからartist_uriをすべてfetchしてlistで返却
    """
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table('spotify-digger')

    scan_result = table.scan()
    artist_uris: List[str] = [
        i["spotify_uri"] for i in scan_result.get("Items")
    ]
    return artist_uris


def put_dynamodb(artist_uri: str) -> None:
    """
    DynamoDBにArtist情報をinsert
    """
    artist_info = spotify.artist(artist_uri)
    item = {
        "name": artist_info["name"],
        "spotify_uri": artist_uri,
        "created_date": datetime.datetime.now().strftime("%Y-%m-%d"),
        "unixtime": int(datetime.datetime.now().timestamp()),  # 小数は不要っぽい
        "url": artist_info["external_urls"]["spotify"]
    }
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table('spotify-digger')
    table.put_item(Item=item)
    return None


def delete_dynamodb(artist_uri: str) -> None:
    """
    DynamoDBからArtist情報をdelete
    """
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table('spotify-digger')
    table.delete_item(Key={'spotify_uri': artist_uri})
    return None
