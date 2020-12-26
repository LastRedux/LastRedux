import sys
import webbrowser

from loguru import logger

import util.new_db_helper as db_helper
from util.NewLastfmApiWrapper import LastfmApiWrapper

lastfm = LastfmApiWrapper()

db_helper.connect()
session = db_helper.get_lastfm_session()

if session:
  lastfm.log_in_with_session(session)
  logger.success(f'Logged in from database as {session.username} with {session.session_key}')
else:
  print('\n***** AUTH TOKEN *****\n')
  auth_token = lastfm.get_auth_token()
  print(f'Token: {auth_token}')

  print('\n***** AUTHORIZE ACCOUNT ACCESS *****\n')
  webbrowser.open(lastfm.generate_authorization_url(auth_token))
  input('(HIT ENTER TO CONTINUE)')

  print('\n***** GET SESSION *****\n')

  try:
    session = lastfm.get_session(auth_token)
    lastfm.log_in_with_session(session)
    print(f'Successfully logged in as {session.username} with {session.session_key}')
    db_helper.save_lastfm_session_to_database(session)
    print('Successfully saved session key and username to database')
  except Exception:
    logger.info(f'Could not get session, auth token not authorized')
    sys.exit(1)

print('\n***** USER INFO *****\n')
print(lastfm.get_user_info())
print(f'Scrobbles today: {lastfm.get_total_scrobbles_today()}')
print(f'Loved tracks: {lastfm.get_total_loved_tracks()}')

print('\n***** RECENT SCROBBLES *****\n')
print(lastfm.get_recent_scrobbles(limit=5))

print('\n***** ARTIST INFO *****\n')
print(lastfm.get_artist_info(artist_name='Madeon'))

print('\n***** TRACK INFO *****\n')
print(lastfm.get_track_info(artist_name='Madeon', track_title='All My Friends'))

print('\n***** ALBUM INFO *****\n')
print(lastfm.get_album_info(artist_name='Madeon', album_title='Good Faith'))

print('\n***** TOP ARTISTS *****\n')
print(lastfm.get_top_artists(limit=5))

print('\n***** TOP ARTISTS THIS WEEK *****\n')
print(lastfm.get_top_artists(limit=5, period='7day'))

print('\n***** TOP TRACKS *****\n')
print(lastfm.get_top_tracks(limit=5))

print('\n***** TOP TRACKS THIS WEEK *****\n')
print(lastfm.get_top_tracks(limit=5, period='7day'))

print('\n***** TOP ALBUMS *****\n')
print(lastfm.get_top_albums(limit=5))

print('\n***** TOP ALBUMS THIS WEEK *****\n')
print(lastfm.get_top_albums(limit=5, period='7day'))

print('\n***** FRIENDS *****\n')

for friend in lastfm.get_friends():
  friend_track = lastfm.get_friend_track(friend_username=friend.username)

  print(friend)
  print(f'{"Now playing" if friend_track and friend_track.is_now_playing else "Last scrobble"}: {friend_track or "N/A"}\n')