from dataclasses import dataclass


@dataclass
class Artist:
    name: str
    url: str
    spotify_uri: str
    image_url: str
    newest_album_url: str