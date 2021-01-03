import os
import time
import json
import hashlib
from datetime import datetime, time

import sentry_sdk
from loguru import logger
import requests

import util.db_helper as db_helper
from util.helpers import generate_system_profile

class LastfmApiWrapper:
  USER_AGENT = 'LastRedux v0.0.0'
  MAX_RETRIES = 3
  NOT_FOUND_ERRORS = ['The artist you supplied could not be found', 'Track not found', 'Album not found']

  def __init__(self, api_key, client_secret):
    # Private attributes
    self.__api_key = api_key
    self.__client_secret = client_secret
    self.__session_key = None
    self.__username = None

  def __generate_method_signature(self, payload):
    '''Create an api method signature from the request payload (in alphabetical order by key) with the client secret
    Example: md5("api_keyxxxxxxxxxxmethodauth.getSessiontokenyyyyyyilovecher")
    '''

    # Remove format key from payload
    data = payload.copy()
    del data['format']

    # Generate param string by concatenating keys and values
    keys = sorted(data.keys())
    param = [key + str(data[key]) for key in keys]

    # Append client secret to the param string
    param = ''.join(param) + self.__client_secret

    # Unicode encode param before hashing
    param = param.encode()

    # Attach the api signature to the payload
    api_sig = hashlib.md5(param).hexdigest()
    
    return api_sig

  def __json_request(self, payload, headers, http_method='GET'):
    '''Make an HTTP request to Last.fm and parse the JSON response'''

    resp = None
    resp_json = None

    if http_method == 'GET':
      # TODO: Handle connection errors
      resp = requests.get('https://ws.audioscrobbler.com/2.0/', headers=headers, params=payload)
    elif http_method == 'POST':
      resp = requests.post('https://ws.audioscrobbler.com/2.0/', headers=headers, data=payload)

    try:
      resp_json = resp.json()
    except json.decoder.JSONDecodeError:
      logger.error(f'Error decoding Last.fm response: {resp.text}')

    return resp_json

  def __lastfm_request(self, payload, key_needed=None, http_method='GET'):
    '''Make an request to Last.fm and attach the needed keys'''

    headers = {'user-agent': self.USER_AGENT}

    payload['api_key'] = self.__api_key
    payload['format'] = 'json'

    if self.__session_key:
      payload['sk'] = self.__session_key

    # Generate method signature after all other keys are added to the payload
    payload['api_sig'] = self.__generate_method_signature(payload)

    resp_json = None

    # Make the request with automatic retries up to a limit
    for i in range(LastfmApiWrapper.MAX_RETRIES):
      resp_json = self.__json_request(payload, headers, http_method)
    
      # Retry request if the key needed in the response is missing (Last.fm sometimes sends back incomplete responses)
      if 'error' in resp_json:
        if resp_json['message'] in LastfmApiWrapper.NOT_FOUND_ERRORS:
          # Not found errors are OK
          break

        logger.error(f'Last.fm request failed to fetch {key_needed} from {payload["method"]}: {resp_json}')
      else:
        break
    else:
      # The key was never found (the for loop completed without breaking)
      logger.error(f'Last.fm fatal failure: Could not fetch {key_needed} from {payload["method"]} after {LastfmApiWrapper.MAX_RETRIES} retries')
    
    # TODO: Handle rate limit condition

    return resp_json

  def __is_logged_in(self):
    if not self.__session_key:
      raise Exception('Last.fm api wrapper not logged in')
    
    return True

  def get_auth_token(self):
    '''Request an authorization token used to get a the session key (lasts 60 minutes)'''
    
    return self.__lastfm_request({
      'method': 'auth.getToken'
    })['token']

  def set_login_info(self, session_key, username):
    system_profile = generate_system_profile()
    
    sentry_sdk.set_context('user', {
      'lastfm_username': username,
      'lastredux_version': 'Private Beta 1',
      **system_profile
    })

    self.__session_key = session_key
    self.__username = username

  def generate_authorization_url(self, auth_token):
    '''Generate a Last.fm authentication url for the user to allow access to their account'''
    
    return f'https://www.last.fm/api/auth/?api_key={self.__api_key}&token={auth_token}'

  def get_session_key_and_username(self, auth_token):
    '''Use an auth token to get the session key and to access the user's account (does not expire)'''
    
    response_json = self.__lastfm_request({
      'method': 'auth.getSession',
      'token': auth_token
    })

    try:
      return response_json['session']['key'], response_json['session']['name']
    except KeyError:
      raise Exception(f'Error loading new session key: {response_json}')

  def get_track_info(self, track):
    '''Get track info about a Scrobble object from a user's Last.fm library'''
    
    if not self.__is_logged_in():
      return

    return self.__lastfm_request({
      'method': 'track.getInfo',
      'track': track.title,
      'artist': track.artist.name,
      'autocorrect': 1,
      'username': self.__username
    })

  def get_album_info(self, artist_name, album_title):
    '''Get album info about a Scrobble object from a user's Last.fm library'''
    
    if not self.__is_logged_in():
      return

    return self.__lastfm_request({
      'method': 'album.getInfo',
      'artist': artist_name,
      'album': album_title,
      'username': self.__username
    })

  def get_artist_info(self, track):
    '''Get artist info about a Scrobble object from a user's Last.fm library'''

    if not self.__is_logged_in():
      return

    return self.__lastfm_request({
      'method': 'artist.getInfo',
      'artist': track.artist.name,
      'username': self.__username,
    })

  def get_friends(self):
    '''Get a list of a the user's friends'''

    if not self.__is_logged_in():
      return 

    return self.__lastfm_request({
      'method': 'user.getFriends',
      'username': self.__username
    })

  def get_recent_scrobbles(self, username=None, count=None):
    '''Get the user's recent scrobbles'''

    # Default parameters cannot refer to self
    if not username:
      username = self.__username

    if not self.__is_logged_in():
      return

    return self.__lastfm_request({
      'method': 'user.getRecentTracks',
      'user': username,
      'extended': 1, # Include artist data in response
      'limit': count
    })

  def get_total_scrobbles_today(self):
    '''Get total scrobbles in the range of the current day'''

    if not self.__is_logged_in():
      return

    # Get the unix timestamp of 12am today
    midnight = int(datetime.combine(datetime.now(), time.min).timestamp()) # Convert to int to trim decimal points (Last.fm 

    resp = self.__lastfm_request({
      'method': 'user.getRecentTracks',
      'user': self.__username,
      'from': midnight,
      'limit': 1
    }, key_needed='recenttracks')

    return int(resp['recenttracks']['@attr']['total'])

  def get_account_details(self):
    '''Get information about the user (total scrobbles, image, registered date, url, etc.)'''

    if not self.__is_logged_in():
      return

    return self.__lastfm_request({
      'method': 'user.getInfo',
      'user': self.__username
    })

  def get_top_tracks(self, period='overall'):
    '''Get a user's top 5 tracks'''

    if not self.__is_logged_in():
      return

    return self.__lastfm_request({
      'method': 'user.getTopTracks',
      'user': self.__username,
      'period': period,
      'limit': 5
    })
  
  def get_top_artists(self, period='overall'):
    '''Get a user's top 5 artists and artists total'''

    if not self.__is_logged_in():
      return

    return self.__lastfm_request({
      'method': 'user.getTopArtists',
      'user': self.__username,
      'period': period,
      'limit': 5
    })

  def get_top_albums(self, period='overall'):
    '''Get a user's top 5 albums'''

    if not self.__is_logged_in():
      return

    return self.__lastfm_request({
      'method': 'user.getTopAlbums',
      'user': self.__username,
      'period': period,
      'limit': 5
    })
  
  def get_total_loved_tracks(self):
    '''Get a user's loved tracks'''

    if not self.__is_logged_in():
      return

    resp_json = self.__lastfm_request({
      'method': 'user.getLovedTracks',
      'user': self.__username,
      'limit': 1 # We don't actually want any loved tracks
    })
    
    return int(resp_json['lovedtracks']['@attr']['total'])

  # POST requests
  def submit_scrobble(self, scrobble):
    '''Send a Scrobble object to Last.fm to save a scrobble to a user\'s profile'''

    if not self.__is_logged_in():
      return

    scrobble_payload = {
      'method': 'track.scrobble',
      'track': scrobble.title,
      'artist': scrobble.artist.name,
      'timestamp': scrobble.timestamp.timestamp() # Convert from datetime object to UTC time
    }

    album_title = scrobble.album.title

    # Only submit album title if it exists
    if album_title:
      scrobble_payload['album'] = album_title

    return self.__lastfm_request(scrobble_payload, http_method='POST')

  def set_track_is_loved(self, scrobble, is_loved):
    '''Set loved value on Last.fm for the passed scrobble'''

    if not self.__is_logged_in():
      return

    return self.__lastfm_request({
      'method': 'track.love' if is_loved else 'track.unlove',
      'track': scrobble.title,
      'artist': scrobble.artist.name
    }, http_method='POST')
  
  def update_now_playing(self, scrobble):
    '''Tell Last.fm to update the user's now playing track'''

    if not self.__is_logged_in():
      return

    scrobble_payload = {
      'method': 'track.updateNowPlaying',
      'track': scrobble.title,
      'artist': scrobble.artist.name,
    }

    album_title = scrobble.album.title

    # Only submit album title if it exists
    if album_title:
      scrobble_payload['album'] = album_title

    return self.__lastfm_request(scrobble_payload, http_method='POST')

# Initialize api wrapper instance with login info once to use in multiple files
__lastfm_instance = None

def get_static_instance():
  global __lastfm_instance
  
  # If there isn't already LastfmApiWrapper instance, create one
  if not __lastfm_instance:
    __lastfm_instance = LastfmApiWrapper('c9205aee76c576c84dc372de469dcb00', 'a643753f16e5c147a0416ecb7bb66eca')

  return __lastfm_instance