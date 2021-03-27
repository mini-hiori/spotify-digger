from dataclasses import dataclass


@dataclass
class Album:
    album_name: str
    album_url: str
    album_image_url: str
    artist_uri: str
    artist_name: str
    artist_url: str
