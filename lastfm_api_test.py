from datetime import date

import util.LastfmApiWrapper as lastfm
import util.db_helper as db_helper

lastfm_instance = lastfm.get_static_instance()

# User info
user_info = lastfm_instance.get_account_details()['user']

real_name = user_info['realname']
username = user_info['name']
total_scrobbles = int(user_info['playcount'])
registered_timestamp = user_info['registered']['#text']
image_url = user_info['image'][-2]['#text'] # Get large size

# Tracks info
overall_tracks_info = lastfm_instance.get_top_tracks()['toptracks']
top_tracks_overall = overall_tracks_info['track']

recent_tracks_info = lastfm_instance.get_top_tracks('7day')['toptracks']
top_tracks_this_week = recent_tracks_info['track']

# Artists info
overall_artists_info = lastfm_instance.get_top_artists()['topartists']
total_artists = int(overall_artists_info['@attr']['total'])
top_artists_overall = overall_artists_info['artist']

recent_artists_info = lastfm_instance.get_top_artists('7day')['topartists']
top_artists_this_week = recent_artists_info['artist']

# Albums info
overall_albums_info = lastfm_instance.get_top_albums()['topalbums']
top_albums_overall = overall_albums_info['album']

recent_albums_info = lastfm_instance.get_top_albums('7day')['topalbums']
top_albums_this_week = recent_albums_info['album']

# Loved track info
total_loved_tracks = lastfm_instance.get_total_loved_tracks()

# Total scrobbles today
total_scrobbles_today = lastfm_instance.get_total_scrobbles_today()

# Calculated stats
total_days_registered = (date.today() - date.fromtimestamp(registered_timestamp)).days
average_daily_scrobbles = round(total_scrobbles / total_days_registered)

print(f'\n***** INFO ABOUT {real_name} (AKA {username}) *****\n')
print(f'{total_scrobbles} scrobbles')
print(f'{total_scrobbles_today} plays today')
print(f'{average_daily_scrobbles} plays per day')
print(f'{total_artists} artists in library')
print(f'{total_loved_tracks} loved tracks')

print('\n***** TOP TRACKS OVERALL *****\n')
for track in top_tracks_overall:
  print(f'{track["name"]} - {track["playcount"]} plays')

print('\n***** TOP TRACKS THIS WEEK *****\n')
for track in top_tracks_this_week:
  print(f'{track["name"]} - {track["playcount"]} plays')

print('\n***** TOP ARTISTS OVERALL *****\n')
for artist in top_artists_overall:
  print(f'{artist["name"]} - {artist["playcount"]} plays')

print('\n***** TOP ARTISTS THIS WEEK *****\n')
for artist in top_artists_this_week:
  print(f'{artist["name"]} - {artist["playcount"]} plays')

print('\n***** TOP ALBUMS OVERALL *****\n')
for album in top_albums_overall:
  print(f'{album["name"]} - {album["playcount"]} plays')

print('\n***** TOP ALBUMS THIS WEEK *****\n')
for album in top_albums_this_week:
  print(f'{album["name"]} - {album["playcount"]} plays')

# Friends
friends = lastfm_instance.get_friends()['friends']['user']

print('\n***** FRIENDS *****\n')

for friend in friends:
  friend_username = friend["name"]
  friend_real_name = friend.get('realname')
  friends_track = None
  
  try:
    friends_track = lastfm_instance.get_recent_scrobbles(friend_username, 1)['recenttracks']['track'][0]
  except IndexError:
    # No friend track
    pass

  if friend_real_name:
    print(f'{friend_real_name} ({friend_username})')
  else:
    print(f'{friend_username}')
  
  if friends_track:
    now_playing = friends_track.get('@attr', {}).get('nowplaying') == 'true'
    track_string = f'{friends_track["artist"]["name"]} - {friends_track["name"]}'

    if now_playing:
      print(f'Now playing: {track_string}')
    else:
      print(f'Last listened to: {track_string}')
  else:
    print('No scrobbles')
    
  print()
