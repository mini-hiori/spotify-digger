from dataclasses import dataclass


@dataclass
class Artist:
    name: str
    url: str
    spotify_uri: str
    image_url: str


@dataclass
class Album:
    name: str
    url: str
    image_url: str
