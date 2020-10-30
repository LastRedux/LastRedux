import re

from loguru import logger
import requests

from datatypes.SpotifyArtist import SpotifyArtist

CLIENT_ID = '26452cc6850d4d1abbd2adb5a6ffccb4'
CLIENT_SECRET = 'b3aee1fc6a584eb89555582ea9bd9d66'
token = ''

def get_token():
  resp = requests.post('https://accounts.spotify.com/api/token', data={
  'grant_type': 'client_credentials'
  }, auth=(CLIENT_ID, CLIENT_SECRET))

  return resp.json()['access_token']

def search_tracks(query):
  return requests.get('https://api.spotify.com/v1/search', params={
    'q': query,
    'type': 'track'
  }, headers={
    'Accept': 'application/json',
    'Authorization': f'Bearer {token}'
  }).json()

def simplify_title(title, is_album=False):
  '''Simplify track and album titles to improve matching on Spotify'''

  # Lowercase to make regex cleaner (Spotify doesn't care about case)
  title = title.lower()

  if is_album:
    # Remove platform specific words for albums
    title = title.replace(' - single', '').replace(' - ep', '').replace('edition', '')
  
  # Remove any text inside brackets (meant to get rid of movie soundtrack labels)
  title = re.sub(r'\[.+\]', '', title)

  # Only allow alphanumeric chars, spaces, asterisks (for censored tracks), and hyphens
  title = re.sub(r'[^A-Za-z0-9\-\* ]+', ' ', title)

  # Remove the world feat
  title = title.replace('feat', '')

  # Cut off censored words at the censor mark for better results (`f**k` turns into `f`)
  title = re.sub('\*+\w+', '', title)

  return title

def simplify_artist_name(artist_name):
  '''Simplify artist name to improve matching on Spotify'''

  # Lowercase artist name to be consistent between platforms (Apple Music doesn't always use correct capitalization for example)
  artist_name = artist_name.lower()

  # Remove ampersands and commas to separate collaborators
  artist_name = artist_name.replace('&', '').replace(',', '')

  return artist_name

def get_images(track_title, artist_name, album_title, no_artists=False):
  global token

  simplified_track_title = simplify_title(track_title)
  simplified_artist_name = simplify_artist_name(artist_name)
  simplified_album_title = '' # Not all tracks have albums
  
  if album_title:
    simplified_album_title = simplify_title(album_title, is_album=True)

  query = f'{simplified_track_title} {simplified_artist_name} {simplified_album_title}'

  search_results = search_tracks(query)

  if 'error' in search_results and search_results['error']['message'] == 'The access token expired':
    logger.trace('Refreshed Spotify access token')
    token = get_token()
    search_results = search_tracks(query)

  if not len(search_results['tracks']['items']):
    # No results
    return

  # Sort tracks by popularity
  sorted_results = sorted(search_results['tracks']['items'], key=lambda k: k['popularity'], reverse=True)
  track = None

  # Find track with matching
  for track_result in sorted_results:
    found = False

    for artist in track_result['artists']:
      if artist['name'].lower() in simplified_artist_name:
        track = track_result
        found = True
        break
    
    if found:
      break

  # Don't search for artists or art if there were no close enough matches
  if not track:
    return

  album_image = track['album']['images'][0]['url']
  album_image_small = track['album']['images'][-1]['url']
  artists = []

  if not no_artists:
    # Make one requests to fetch data for all artists
    artists_resp = requests.get('https://api.spotify.com/v1/artists/', params={
      'ids': ','.join([artist['id'] for artist in track['artists']]) # Create comma separated list of Spotify artist ids
    },
    headers={
      'Accept': 'application/json',
      'Authorization': f'Bearer {token}'
    })

    artists_json = artists_resp.json()

    for artist in artists_json['artists']:
      artist_image = artist['images'][-1]['url'] if artist['images'] else ''
      
      artists.append(
        SpotifyArtist(
          name=artist['name'], 
          spotify_url=artist['external_urls']['spotify'], 
          image_url=artist_image
        )
      )

  return artists, album_image, album_image_small

if not token:
  token = get_token()
