import urllib

import requests

def get_itunes_store_album_images(track_title, artist_name, album_title=''):
  '''Get art for an album from the iTunes Search API'''

  # Escape special characters in query string
  escaped_search_term = urllib.parse.quote(f'{artist_name} {track_title} {album_title}')

  # Do a generic search for music with the track, artist, and album name
  track_response = requests.get(f'https://itunes.apple.com/search?media=music&limit=1&term={escaped_search_term}')

  if not track_response.ok:
    raise Exception(f'Error getting iTunes store images: {track_response.text}')
    return

  track_results = track_response.json()['results']

  # Return an empty object if there are no results for the track (local file)
  if not track_results:
    return

  # Get album art url at 30x30
  album_image = track_results[0]['artworkUrl30'].replace('30x30', '300x300')
  album_image_small = track_results[0]['artworkUrl30'].replace('30x30', '64x64')

  return album_image, album_image_small