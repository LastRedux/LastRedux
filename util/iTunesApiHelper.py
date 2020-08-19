import re

import requests

def __get_artist_image_from_artist_url(artist_url):
  '''Scrape an Apple Music artist url at the default size'''

  return requests.get(artist_url).text.split('srcset')[1].split('>')[0].split(', ')[1].split('"')[0].split(' ')[0]

def __format_image_url_to_size(image_url, width, height):
  '''Replace the dimensions in an iTunes image url with a size'''

  return re.sub(r'\d+x\d+', f'{width}x{height}', image_url)

def get_images(track_name, artist_name, album_name):
  '''Get an artist image and album art for a track from the iTunes Search API'''

  # Do a generic search for music with the track, artist, and album name
  track_results = requests.get(f'https://itunes.apple.com/search?media=music&limit=1&term={artist_name} {track_name} {album_name}').json()['results']

  # Return an empty object if there are no results for the track (local file)
  if not track_results:
    return None

  # Scrape the Apple Music website HTML for artist image
  artist_image = __get_artist_image_from_artist_url(track_results[0]['artistViewUrl'])

  # Get album art url at 30x30
  album_art = track_results[0]['artworkUrl30']

  # Swap out dimensions in image URLs
  artist_image = __format_image_url_to_size(artist_image, 256, 256)
  album_art = __format_image_url_to_size(album_art, 300, 300)
  album_art_small = __format_image_url_to_size(album_art, 64, 64)

  return artist_image, album_art, album_art_small

def get_artist_image(artist_name):
  '''Get an artist image by name from the iTunes Search API'''

  # Do a generic search for music with the track, artist, and album name
  artist_results = requests.get(f'https://itunes.apple.com/search?media=music&entity=musicArtist&attribute=artistTerm&limit=1&term={artist_name}').json()['results']

  # Return an empty object if there are no results for the track (local file)
  if not artist_results:
    return None

  return __get_artist_image_from_artist_url(artist_results[0]['artistLinkUrl'])