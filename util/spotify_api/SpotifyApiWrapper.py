import re

from unidecode import unidecode
from loguru import logger
import requests

from datatypes.ImageSet import ImageSet
from .SpotifyImages import SpotifyImages
from .SpotifyArtist import SpotifyArtist

class SpotifyApiWrapper:
  CLIENT_ID = '26452cc6850d4d1abbd2adb5a6ffccb4'
  CLIENT_SECRET = 'b3aee1fc6a584eb89555582ea9bd9d66'

  def __init__(self):
    # Store Spotify access token
    self.access_token: str = self.__get_access_token()

  def get_images(self, artist_name: str, track_title: str, album_title: str=None, no_artists: bool=False) -> dict:
    '''Get album art and artist images from Spotify by track'''

    # Search Spotify using a generic and platform-agnostic query
    results = self.__search_tracks(
      artist_name=SpotifyApiWrapper.__simplify_artist_name(artist_name),
      track_title=SpotifyApiWrapper.__simplify_title(track_title),
      album_title=SpotifyApiWrapper.__simplify_title(album_title) if album_title else ''
    )

    if 'error' in results:
      if results['error']['message'] == 'The access token expired':
        # Generate a new access token (lasts for 1 hour by default)
        self.access_token = SpotifyApiWrapper.__get_access_token()
        logger.trace('Refreshed Spotify access token')

        # Retry request
        self.get_images(artist_name, track_title, album_title, no_artists)
        return
      else:
        logger.error(f'Spotify search error: {results}')

    track_results = results['tracks']['items']

    if not len(track_results):
      # No results
      return None

    track = None

    # Find track with matching
    for track_result in track_results:
      found = False

      for artist in track_result['artists']:
        # Check if nuked artist name from Spotify is in the list of artists (Apple Music formats collaboration as a string of artist names)
        nuked_artist_string = SpotifyApiWrapper.__nuke_artist_name(artist_name)
        if SpotifyApiWrapper.__nuke_artist_name(artist['name']) in nuked_artist_string:
          track = track_result
          found = True
          break
      
      if found:
        break

    # Don't search for artists or art if there were no close enough matches
    if not track:
      return None

    artist_objects = []

    if not no_artists:
      # Make one requests to fetch data for all artists
      artists_resp = requests.get('https://api.spotify.com/v1/artists/', params={
        'ids': ','.join([artist['id'] for artist in track['artists']]) # Create comma separated list of Spotify artist ids
      },
      headers={
        'Accept': 'application/json',
        'Authorization': f'Bearer {self.access_token}'
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
            url=artist['external_urls']['spotify'], 
            image_url=artist_image
          )
        )

    return SpotifyImages(
      artists=artist_objects,
      album_art=ImageSet(
        small_url=track['album']['images'][-1]['url'],
        medium_url=track['album']['images'][-2]['url'] #TODO: Get the index right
      )
    )
    
  # --- Private Methods ---

  def __search_tracks(self, artist_name: str, track_title: str, album_title:str) -> dict:
    return requests.get('https://api.spotify.com/v1/search', params={
      'q': f'{track_title} {artist_name} {album_title}',
      'type': 'track'
    }, headers={
      'Accept': 'application/json',
      'Authorization': f'Bearer {self.access_token}'
    }).json()

  @staticmethod
  def __get_access_token() -> dict:
    '''Get an access token from Spotify using client credentials authentication'''

    return requests.post('https://accounts.spotify.com/api/token', data={
      'grant_type': 'client_credentials'
    }, auth=(SpotifyApiWrapper.CLIENT_ID, SpotifyApiWrapper.CLIENT_SECRET)).json()['access_token']

  @staticmethod
  def __simplify_title(title: str) -> str:
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

  @staticmethod
  def __simplify_artist_name(artist_name: str) -> str:
    '''
    Simplify artist name to improve matching on Spotify
    
    Example:
    in: 'J Balvin, Dua Lipa, Bad Bunny & Tainy'
    out: 'j balvin dua lipa bad bunny tainy'
    '''

    # Lowercase artist name to be consistent between platforms (Apple Music doesn't always use correct capitalization for example)
    artist_name = artist_name.lower()

    # Remove ampersands and commas to separate collaborators
    artist_name = artist_name.replace('& ', '').replace(',', '')

    return artist_name

  @staticmethod
  def __nuke_artist_name(artist_name: str) -> str:
    '''
    Totally reduce artist name to check matches between a simplified string and a list of individual artists
    
    Example:
    in: J Balvin, Dua Lipa, Bad Bunny & Tainy
    out: jbalvindualipabadbunnytainy

    Example:
    in: J Balvin
    out: jbalvin (which is in jbalvindualipabadbunnytainy)
    '''

    return re.sub(r'[^a-zA-Z0-9]+', '', artist_name.lower())