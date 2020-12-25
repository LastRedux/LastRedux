import util.LastfmApiWrapper as lastfm

lastfm_instance = lastfm.get_static_instance()

print(f'\n***** USER INFO *****\n')
print(lastfm_instance.get_user_info())
print(f'Scrobbles today: {lastfm_instance.get_total_scrobbles_today()}')
print(f'Loved tracks: {lastfm_instance.get_total_loved_tracks()}')

print('\n***** TRACK INFO *****\n')
print(lastfm_instance.get_track_info(artist_name='Madeon', track_title='All My Friends'))

print('\n***** ARTIST INFO *****\n')
print(lastfm_instance.get_artist_info(artist_name='Madeon'))

print('\n***** ALBUM INFO *****\n')
print(lastfm_instance.get_album_info(artist_name='Madeon', album_title='Good Faith'))

print('\n***** TOP ARTISTS *****\n')
print(lastfm_instance.get_top_artists(limit=5))

print('\n***** TOP ARTISTS THIS WEEK *****\n')
print(lastfm_instance.get_top_artists(limit=5, period='7day'))

print('\n***** TOP TRACKS *****\n')
print(lastfm_instance.get_top_tracks(limit=5))
print('\n***** TOP TRACKS THIS WEEK *****\n')
print(lastfm_instance.get_top_tracks(limit=5, period='7day'))

print('\n***** TOP ALBUMS *****\n')
print(lastfm_instance.get_top_albums(limit=5))

print('\n***** TOP ALBUMS THIS WEEK *****\n')
print(lastfm_instance.get_top_albums(limit=5, period='7day'))

print('\n***** FRIENDS *****\n')
friends = lastfm_instance.get_friends()

for friend in friends:
  friend_track = lastfm_instance.get_friend_track(friend_username=friend.username)

  print(friend)
  print(f'{"Now playing" if friend_track and friend_track.is_now_playing else "Last scrobble"}: {friend_track or "N/A"}\n')