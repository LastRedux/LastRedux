import re
import urllib

import requests

def __get_artist_image_from_artist_url(artist_url):
  '''Scrape an Apple Music artist url at the default size'''

  return requests.get(artist_url).text.split('srcset')[1].split('>')[0].split(', ')[1].split('"')[0].split(' ')[0]

def __format_image_url_to_size(image_url, width, height):
  '''Replace the dimensions in an iTunes image url with a size'''

  return re.sub(r'\d+x\d+', f'{width}x{height}', image_url)

def get_images(track_title, artist_name, album_title):
  '''Get an artist image and album art for a track from the iTunes Search API'''

  print(f'Requesting images from iTunes Search API: {track_title}')

  # Replace the None value with an empty string for the search term
  if not album_title:
    album_title = ''

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

  # Scrape the Apple Music website HTML for artist image
  artist_image = __get_artist_image_from_artist_url(track_results[0]['artistViewUrl'])

  # Get album art url at 30x30
  album_image_url = track_results[0]['artworkUrl30']

  # Swap out dimensions in image URLs
  artist_image = __format_image_url_to_size(artist_image, 256, 256)
  album_image_url = __format_image_url_to_size(album_image_url, 300, 300)
  album_art_small = __format_image_url_to_size(album_image_url, 64, 64)

  return artist_image, album_image_url, album_art_small