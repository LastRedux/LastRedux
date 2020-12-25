import re

from unidecode import unidecode
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

def simplify_title(title):
  '''
  Simplify track and album titles to improve matching on Spotify
  
  Example:
  in: 'FRANCHISE (feat. Young Thug & M.I.A.) - Single'
  out: 'franchise    young thug   m i a '
  '''

  # Lowercase title and remove diacriticals to make regex cleaner (Spotify doesn't care about case)
  title = unidecode(title.lower())

  # Remove special keywords (before regex in case one of the keywords is actually in the name)
  title = title.replace(' - single', '').replace(' - ep', '').replace('edition', '')
  
  # Remove any text inside brackets (meant to get rid of movie soundtrack labels)
  title = re.sub(r'\[from.+\]', '', title)

  # Only allow alphanumeric chars, spaces, asterisks (for censored tracks), and hyphens
  title = re.sub(r'[^A-Za-z0-9\-\* ]+', ' ', title)

  # Remove the world featuring/feat
  title = title.replace('featuring', '')
  title = title.replace('feat', '')

  # Cut off censored words at the censor mark for better results (`f**k` turns into `f`)
  title = re.sub('\*+\w+', '', title)

  # Remove general keywords
  title = title.replace('album version', '')

  return title

def simplify_artist_name(artist_name):
  '''
  Simplify artist name to improve matching on Spotify
  
  Example:
  in: 'J Balvin, Dua Lipa, Bad Bunny & Tainy'
  out: 'j balvin dua lipa bad bunny  tainy'
  '''

  # Lowercase artist name to be consistent between platforms (Apple Music doesn't always use correct capitalization for example)
  artist_name = artist_name.lower()

  # Remove ampersands and commas to separate collaborators
  artist_name = artist_name.replace('&', '').replace(',', '')

  return artist_name

def nuke_artist_name(artist_name):
  '''
  Totally reduce artist name to check matches between a simplified string and a list of individual artists
  
  Example:
  in: J Balvin, Dua Lipa, Bad Bunny & Tainy
  out: jbalvindualipabadbunnytainy

  Example:
  in: J Balvin
  out: jbalvin (which is in jbalvindualipabadbunnytainy)
  '''

  return artist_name.lower().replace('.', '').replace(' ', '').replace('-', '').replace('–', '').replace('/', '').replace('\\', '').replace('&', '').replace(',', '')

def get_images(track_title, artist_name, album_title, no_artists=False):
  global token

  simplified_track_title = simplify_title(track_title)
  simplified_artist_name = simplify_artist_name(artist_name)
  simplified_album_title = '' # Not all tracks have albums
  
  if album_title:
    simplified_album_title = simplify_title(album_title)

  query = f'{simplified_track_title} {simplified_artist_name} {simplified_album_title}'

  search_resp = search_tracks(query)

  if 'error' in search_resp:
    if search_resp['error']['message'] == 'The access token expired':
      logger.trace('Refreshed Spotify access token')
      token = get_token()
      search_resp = search_tracks(query)
    else:
      logger.error(f'Spotify search error: {search_resp}')

  track_results = search_resp['tracks']['items']

  if not len(track_results):
    # No results
    return

  track = None

  # Find track with matching
  for track_result in track_results:
    found = False

    for artist in track_result['artists']:
      # Compare simplified artist names to make sure they match
      if nuke_artist_name(artist['name']) in nuke_artist_name(simplified_artist_name):
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
  artist_objects = []

  if not no_artists:
    # Make one requests to fetch data for all artists
    artists_resp = requests.get('https://api.spotify.com/v1/artists/', params={
      'ids': ','.join([artist['id'] for artist in track['artists']]) # Create comma separated list of Spotify artist ids
    },
    headers={
      'Accept': 'application/json',
      'Authorization': f'Bearer {token}'
    })

    artists = artists_resp.json()['artists']

    for artist in artists:      
      images = artist['images']
      artist_image = ''
      
      # Some Spotify artists don't have an image
      if images:
        if len(artists) > 1:
          # Get small size if there is more than one artist
          artist_image = images[-1]['url']
        else:
          # Get large size if there is only one artist
          artist_image = images[-2]['url']
      
      artist_objects.append(
        SpotifyArtist(
          name=artist['name'], 
          spotify_url=artist['external_urls']['spotify'], 
          image_url=artist_image
        )
      )

  return artist_objects, album_image, album_image_small

if not token:
  token = get_token()
