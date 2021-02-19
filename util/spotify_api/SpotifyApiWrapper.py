import logging
import json
import re
import os
from typing import Dict, List

from unidecode import unidecode
import requests

from datatypes.ImageSet import ImageSet
from .SpotifySongData import SpotifySongData
from .SpotifyArtist import SpotifyArtist
from datatypes.CachedResource import CachedResource

class SpotifyApiWrapper:
  CLIENT_ID = '26452cc6850d4d1abbd2adb5a6ffccb4'
  CLIENT_SECRET = 'b3aee1fc6a584eb89555582ea9bd9d66'

  def __init__(self) -> None:
    # Store Spotify access token
    self.__access_token: str = None
    self.__ram_cache: Dict[str, CachedResource] = {}

  # --- Search Wrappers ---
  
  def get_artist(self, artist_name: str) -> SpotifyArtist:
    results = self.__search(
      query=SpotifyApiWrapper.__simplify_artist_name(artist_name),
      media_type='artist',
      limit=1
    )

    if not results:
      logging.warning(f'No Spotify artist results for "{artist_name}"')
      return

    image_url = None

    try:
      image_url = results[0]['images'][-1]['url']
    except IndexError:
      # No images
      image_url = None

    return SpotifyArtist(
      url=results[0]['external_urls']['spotify'],
      name=artist_name,
      image_url=image_url
    )

  def get_track_images(self,
    artist_name: str,
    track_title: str=None, # Some searches are only for an album
    album_title: str=None, # Some searches are only for a track
    only_album_art: bool=False,
    is_retry: bool=False
  ) -> SpotifySongData:
    # Create empty return type
    spotify_data = SpotifySongData(None, None)

    query = '{} {} {}'.format(
      SpotifyApiWrapper.__simplify_artist_name(artist_name),
      SpotifyApiWrapper.__simplify_title(track_title) if track_title else '',
      SpotifyApiWrapper.__simplify_title(album_title) if album_title else '' 
    )

    # Remove extra spaces from query
    query = ' '.join(query.split())

    results = self.__search(
      query=query,
      media_type='track'
    )

    if results:
      track = self.__find_track_match(results, artist_name)

      # Find track with matching artists
      if track:
        spotify_data.album_art = ImageSet(
          small_url=track['album']['images'][-1]['url'],
          medium_url=track['album']['images'][-2]['url'] #TODO: Get the index right
        )

        if not only_album_art:
          artists = self.__get_artists_by_id(track['artists'])

          spotify_data.artists = [
            SpotifyArtist(
              name=artist['name'],
              url=artist['external_urls']['spotify'],
              image_url=(
                # Get small image if there is more than one artist
                artist['images'][-1]['url'] if len(artists) > 1 else artist['images'][-2]['url']
              ) if artist['images'] else None
            ) for artist in artists
          ]
    else:
      # Try new search with no album title (useful for pre-release albums or any other mismatch between platforms)
      if not is_retry and album_title:
        return self.get_track_images(artist_name, track_title, None, only_album_art, is_retry=True) # Retry 0 because the parameters have changed
      else:
        logging.warning(f'No Spotify track results for "{query}"')

    return spotify_data
    
  # --- Private Methods ---

  def __search(self, query: str, media_type: str, limit: int=20) -> ImageSet:
    result = self.__request(
      url='https://api.spotify.com/v1/search/',
      args={
        'q': query,
        'type': media_type,
        'limit': limit
      }
    )
    
    if not result:
      return None
    
    return result.get(f'{media_type}s', {}).get('items')

  def __request(self, url: str, args: dict, is_retry=False) -> dict:
    '''Make a request to Spotify and handle the potential errors'''

    # Convert request arguments to string to use as a key to the cache
    request_string = json.dumps(args, sort_keys=True)

    # Check for cached responses
    if request_string in self.__ram_cache:
      logging.debug(f'Used Spotify API cache: {url} {args}')

      return self.__ram_cache[request_string].data

    resp = None

    if not self.__access_token:
      self.__access_token = self.__get_access_token()
    
    try:
      resp = requests.get(
        url=url,
        params=args, 
        headers={
          'Accept': 'application/json',
          'Authorization': f'Bearer {self.__access_token}'
        }
      )
    except (ConnectionResetError, ConnectionError):
      # Retry one time (Spotify doesn't usually have connection problems)
      if not is_retry:
        self.__request(url, args, is_retry=True)
      else:
        logging.error('Could not connect to Spotify')
      
      return

    resp_json = resp.json()

    if 'error' in resp_json:
      if resp_json['error']['message'] == 'The access token expired':
        # Generate a new access token (lasts for 1 hour by default)
        self.__access_token = SpotifyApiWrapper.__get_access_token()
        logging.debug('Refreshed Spotify access token')

        # Retry request
        self.__request(url, args)
        return
      elif resp_json['error']['status'] == 502:
        # Retry request
        self.__request(url, args)
        return
      else:
        raise Exception(f'Spotify search error: {resp_json}')
    
    self.__ram_cache[request_string] = CachedResource(
      data=resp_json,
      expiration_date=None # Spotify data shouldn't change
    )

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