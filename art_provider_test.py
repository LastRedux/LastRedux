import sys
import json

from loguru import logger

from util.lastfm import LastfmApiWrapper
from util.spotify_api import SpotifyApiWrapper
import util.db_helper as db_helper
from util.art_provider import ArtProvider

lastfm = LastfmApiWrapper()

db_helper.connect()

# Try to get session key and username from database
session = db_helper.get_lastfm_session()

if session:
  # Set Last.fm wrapper session key and username from database
  lastfm.log_in_with_session(session)
  logger.success(f'Logged in from database as {session.username}')
else:
  logger.error('No login details saved, run lastfm_api_test.py to save a session to the database')
  sys.exit(1)

art_provider = ArtProvider(lastfm)
spotify_api = SpotifyApiWrapper()

print('\n***** SPOTIFY ARTISTS *****\n')
print(spotify_api.get_artist('RIOT'))
print(spotify_api.get_artist('Ariana Grande'))
print(spotify_api.get_artist('Madeon'))

print('\n***** ALBUM ART AND ARTIST IMAGES (MOCK TRACKS) *****\n')
for mock_track in json.load(open('mock_data/mock_tracks.json')):
  # Remove unneeded key for unpacking later
  del mock_track['reason']

  print(f'** {mock_track["artist_name"]} - {mock_track["track_title"]} | {mock_track.get("album_title", None)} ** ')

  # Search Spotify for album art and artist images
  print('Spotify results:')
  print(spotify_api.get_track_images(**mock_track))

  # Search Last.fm
  if 'album_title' not in mock_track:
    continue

  image_set = art_provider.get_album_art(**mock_track)

  print('\nAlbum art results:')
  if image_set:
    print(image_set)
  else:
    print('No album art found')
  
  # Separator
  print()