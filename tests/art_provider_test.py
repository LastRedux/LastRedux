import sys
import json

from util.lastfm import LastfmApiWrapper
from util.spotify_api import SpotifyApiWrapper
import util.db_helper as db_helper
from util.AlbumArtProvider import AlbumArtProvider

lastfm = LastfmApiWrapper()
spotify_api = SpotifyApiWrapper()

db_helper.connect()

# Try to get session key and username from database
session = db_helper.get_lastfm_session()

if session:
  # Set Last.fm wrapper session key and username from database
  lastfm.log_in_with_session(session)
  print('Logged in from database')
else:
  print('No login details saved, run lastfm_api_test.py to save a session key and username to the database')
  sys.exit(1)

art_provider = AlbumArtProvider(lastfm, spotify_api)

for mock_track in json.load(open('mock_data/mock_tracks.json')):
  if 'album_title' not in mock_track:
    continue

  print(f'\n{mock_track["artist_name"]} | {mock_track["album_title"]}')

  image_set = art_provider.get_album_art(
    artist_name=mock_track['artist_name'],
    track_title=mock_track['track_title'],
    album_title=mock_track['album_title']
  )

  if image_set:
    print(image_set)
  else:
    print('No album art found')