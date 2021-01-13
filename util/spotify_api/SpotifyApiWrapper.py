import re
from typing import List

from unidecode import unidecode
from loguru import logger
import requests

from datatypes.ImageSet import ImageSet
from .SpotifyImages import SpotifyImages
from .SpotifyArtist import SpotifyArtist

class SpotifyApiWrapper:
  CLIENT_ID = '26452cc6850d4d1abbd2adb5a6ffccb4'
  CLIENT_SECRET = 'b3aee1fc6a584eb89555582ea9bd9d66'

  def __init__(self) -> None:
    # Store Spotify access token
    self.access_token: str = self.__get_access_token()

  # --- Search Wrappers ---
  
  def get_artist(self, artist_name: str) -> SpotifyArtist:
    results = self.__search(
      query=SpotifyApiWrapper.__simplify_artist_name(artist_name),
      media_type='artist',
      limit=1
    )['artists']['items']

    if not len(results):
      return None

    return SpotifyArtist(
      url=results[0]['external_urls']['spotify'],
      name=artist_name,
      image_url=results[0]['images'][-1]['url']
    )

  def get_track_images(self,
    artist_name: str,
    track_title: str,
    album_title: str=None,
    only_album_art: bool=False
  ) -> SpotifyImages:
    results = self.__search(
      query='{} {} {}'.format(
        SpotifyApiWrapper.__simplify_artist_name(artist_name),
        SpotifyApiWrapper.__simplify_title(track_title) if track_title else '',
        SpotifyApiWrapper.__simplify_title(album_title) if album_title else ''
      ),
      media_type='track'
    )['tracks']['items']

    if not len(results):
      return None

    track = self.__find_track_match(results, artist_name)

    # Find track with matching artists
    if not track:
      return None

    album_art = ImageSet(
      small_url=track['album']['images'][-1]['url'],
      medium_url=track['album']['images'][-2]['url'] #TODO: Get the index right
    )

    if only_album_art:
      return album_art

    artists = self.__get_artists_by_id(track['artists'])

    return SpotifyImages(
      artists=[
        SpotifyArtist(
          name=artist['name'],
          url=artist['external_urls']['spotify'],
          image_url=(
            # Get small image if there is more than one artist
            artist['images'][-1]['url'] if len(artists) > 1 else artist['images'][-2]['url']
          ) if artist['images'] else None
        ) for artist in artists
      ],
      album_art=album_art
    )
    
  # --- Private Methods ---

  def __search(self, query: str, media_type: str, limit: int=20) -> ImageSet:
    return self.__request(
      url='https://api.spotify.com/v1/search/',
      args={
        'q': query,
        'type': media_type,
        'limit': limit
      }
    )

  def __request(self, url: str, args: dict) -> dict:
    '''Make a request to Spotify and handle the potential errors'''

    resp_json = requests.get(
      url=url,
      params=args, 
      headers={
        'Accept': 'application/json',
        'Authorization': f'Bearer {self.access_token}'
      }
    ).json()

    if 'error' in resp_json:
      if resp_json['error']['message'] == 'The access token expired':
        # Generate a new access token (lasts for 1 hour by default)
        self.access_token = SpotifyApiWrapper.__get_access_token()
        logger.trace('Refreshed Spotify access token')

        # Retry request
        self.__request(url, args)
        return
      else:
        raise Exception(f'Spotify search error: {resp_json}')

    return resp_json

  @staticmethod
  def __find_track_match(results: List[dict], artist_string: str) -> dict:
    '''Select a match from a list of Spotify search results'''
    
    for match in results:
      for artist in match['artists']:
        # Check if the artist from Spotify is in the list of artist names
        # (Apple Music formats collaborations as a string of comma separated names)
        nuked_artist_string = SpotifyApiWrapper.__nuke_artist_name(artist_string)
        nuked_spotify_artist = SpotifyApiWrapper.__nuke_artist_name(artist['name'])
        
        if nuked_spotify_artist in nuked_artist_string:
          return match

    return None

  def __get_artists_by_id(self, artists: List[dict]) -> List[SpotifyArtist]:
    return self.__request(
      url='https://api.spotify.com/v1/artists/',
      args={
        # Create comma separated list of Spotify artist ids
        'ids': ','.join([artist['id'] for artist in artists])
      }
    )['artists']

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