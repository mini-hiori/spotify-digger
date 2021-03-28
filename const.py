import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import boto3

ssm = boto3.client('ssm')
client_id = ssm.get_parameter(
        Name='SpotifyClientID'
)['Parameter']['Value']
client_secret = ssm.get_parameter(
        Name='SpotifyClientSecret',
        WithDecryption=True
)['Parameter']['Value']
client_credentials_manager = spotipy.oauth2.SpotifyClientCredentials(
    client_id, client_secret)

spotify = spotipy.Spotify(
    client_credentials_manager=client_credentials_manager)
webhook_url = ssm.get_parameter(
        Name='SpotifyDiggerDiscordWebhookURL'
)['Parameter']['Value']