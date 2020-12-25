from datatypes.lastfm.LastfmFullAlbum import LastfmFullAlbum
import os
import time
import json
import hashlib
from datetime import datetime, time
from typing import List

from loguru import logger
import requests

import util.db_helper as db_helper
from datatypes.lastfm.LastfmUserInfo import LastfmUserInfo
from datatypes.lastfm.LastfmTopArtists import LastfmTopArtists
from datatypes.lastfm.LastfmTopArtist import LastfmTopArtist
from datatypes.lastfm.LastfmTracks import LastfmTracks
from datatypes.lastfm.LastfmHistoryTrack import LastfmHistoryTrack
from datatypes.lastfm.LastfmTopTrack import LastfmTopTrack
from datatypes.lastfm.LastfmTopAlbums import LastfmTopAlbums
from datatypes.lastfm.LastfmTopAlbum import LastfmTopAlbum
from datatypes.lastfm.LastfmUser import LastfmUser
from datatypes.lastfm.LastfmFriendTrack import LastfmFriendTrack
from datatypes.lastfm.LastfmArtist import LastfmArtist
from datatypes.lastfm.LastfmFullArtist import LastfmFullArtist
from datatypes.lastfm.LastfmTags import LastfmTags
from datatypes.lastfm.LastfmTag import LastfmTag
from datatypes.lastfm.LastfmFullTrack import LastfmFullTrack
from datatypes.lastfm.LastfmArtists import LastfmArtists

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

  # --- Request Wrappers ---

  def get_user_info(self) -> LastfmUserInfo:
    return self.__lastfm_request({
        'method': 'user.getInfo',
        'username': self.__username
      },
      main_key_getter=lambda response: response['user'],
      return_value_builder=lambda user_info, response: LastfmUserInfo(
        username=user_info['name'],
        real_name=user_info['realname'],
        image_url=user_info['image'][-1]['#text'].replace('300', '500'),
        image_url_small=user_info['image'][-2]['#text'],
        url=user_info['url'],
        registered_timestamp=int(user_info['registered']['unixtime']),
        total_scrobbles=int(user_info['playcount'])
      )
    )

  def get_top_artists(self, limit, period='overall') -> LastfmTopArtists:
    return self.__lastfm_request({
        'method': 'user.getTopArtists',
        'username': self.__username,
        'limit': limit,
        'period': period
      },
      main_key_getter=lambda response: response['topartists']['artist'],
      return_value_builder=lambda artists, response: LastfmTopArtists(
        artists=[LastfmTopArtist(
          name=artist['name'],
          plays=int(artist['playcount']),
          url=artist['url']
        ) for artist in artists],
        total=response['topartists']['@attr']['total']
      )
    )

  def get_top_tracks(self, limit, period='overall') -> LastfmTracks:
    return self.__lastfm_request({
        'method': 'user.getTopTracks',
        'username': self.__username,
        'limit': limit,
        'period': period
      },
      main_key_getter=lambda response: response['toptracks']['track'],
      return_value_builder=lambda tracks, response: LastfmTracks(
        tracks=[LastfmTopTrack(
          title=track['name'],
          artist_name=track['artist']['name'],
          url=track['url'],
          plays=track['playcount']
        ) for track in tracks],
        total=response['toptracks']['@attr']['total']
      )
    )

  def get_top_albums(self, limit, period='overall') -> LastfmTopAlbums:
    return self.__lastfm_request({
        'method': 'user.getTopAlbums',
        'username': self.__username,
        'limit': limit,
        'period': period
      },
      main_key_getter=lambda response: response['topalbums']['album'],
      return_value_builder=lambda albums, response: LastfmTopAlbums(
        albums=[LastfmTopAlbum(
          title=album['name'],
          artist_name=album['artist']['name'],
          url=album['url'],
          plays=album['playcount']
        ) for album in albums],
        total=int(response['topalbums']['@attr']['total'])
      )
    )

  def get_recent_scrobbles(self, limit, from_timestamp=None, username=None) -> LastfmTracks:
    return self.__lastfm_request({
        'method': 'user.getRecentTracks',
        'username': username or self.__username, # Default arg value can't refer to self
        'from': from_timestamp
      },
      main_key_getter=lambda response: response['recenttracks']['track'],
      return_value_builder=lambda tracks, response: LastfmTracks(
        tracks=[LastfmHistoryTrack(
          title=track['name'],
          artist_name=track['artist']['#text'],
          url=track['url']
        ) for track in tracks],
        total=response['recenttracks']['@attr']['total']
      )
    )

  def get_total_loved_tracks(self) -> int:
    return self.__lastfm_request({
        'method': 'user.getLovedTracks',
        'user': self.__username,
        'limit': 1 # We don't actually want any loved tracks
      },
      return_value_builder=lambda response: response['lovedtracks']['@attr']['total']
    )

  def get_friends(self) -> List:
    return self.__lastfm_request({
        'method': 'user.getFriends',
        'username': self.__username
      },
      main_key_getter=lambda response: response['friends']['user'],
      return_value_builder=lambda friends, response: [
        LastfmUser(
          username=friend['name'],
          real_name=friend['realname'],
          image_url=friend['image'][2]['#text'],
          image_url_small=friend['image'][-2]['#text'],
          url=friend['url']
        ) for friend in friends
      ]
    )

  def get_friend_track(self, friend_username):
    return self.__lastfm_request({
        'method': 'user.getRecentTracks',
        'username': friend_username
      },
      main_key_getter=lambda response: response['recenttracks']['track'][0] if len(response['recenttracks']['track']) else None, # Not all users have a scrobble
      return_value_builder=lambda track, response: LastfmFriendTrack(
        title=track['name'],
        artist_name=track['artist']['#text'],
        url=track['url'],
        is_now_playing=track.get('@attr', {}).get('nowplaying') == 'true'
      ) if track else None
    )
  
  def get_artist_info(self, artist_name):
    return self.__lastfm_request({
        'method': 'artist.getInfo',
        'username': self.__username,
        'artist': artist_name
      },
      main_key_getter=lambda response: response['artist'],
      return_value_builder=lambda artist, response: LastfmFullArtist(
        name=artist['name'],
        url=artist['url'],
        plays=int(artist['stats']['userplaycount']),
        global_listeners=int(artist['stats']['listeners']),
        global_plays=int(artist['stats']['playcount']),
        bio=artist['bio']['summary'],
        tags=LastfmTags(
          tags=[self.__tag_to_lastfm_tag(tag) for tag in artist['tags']['tag']]
        ),
        similar_artists=LastfmArtists(
          artists=[
            LastfmArtist(
              name=similar_artist['name'],
              url=similar_artist['url']
            ) for similar_artist in artist['similar']['artist']
          ]
        )
      )
    )

  def get_track_info(self, artist_name, track_title):
    return self.__lastfm_request({
        'method': 'track.getInfo',
        'username': self.__username,
        'artist': artist_name,
        'track': track_title
      },
      main_key_getter=lambda response: response['track'],
      return_value_builder=lambda track, response: LastfmFullTrack(
        title=track['name'],
        artist_name=track['artist']['name'],
        url=track['url'],
        plays=int(track['userplaycount']),
        is_loved=bool(int(track['userloved'])), # Convert '0'/'1' to False/True,
        global_listeners=int(track['listeners']),
        global_plays=int(track['playcount']),
        tags=LastfmTags(
          tags=[self.__tag_to_lastfm_tag(tag) for tag in track['toptags']['tag']]
        )
      )
    )

  def get_album_info(self, artist_name, album_title):
    return self.__lastfm_request({
        'method': 'album.getInfo',
        'username': self.__username,
        'artist': artist_name,
        'album': album_title
      },
      main_key_getter=lambda response: response['album'],
      return_value_builder=lambda album, response: LastfmFullAlbum(
        title=album['name'],
        artist_name=album['artist'],
        url=album['url'],
        plays=int(album['userplaycount']),
        global_listeners=int(album['listeners']),
        global_plays=int(album['playcount']),
        tags=LastfmTags(
          tags=[self.__tag_to_lastfm_tag(tag) for tag in album['tags']['tag']]
        )
      )
    )

  # # POST requests
  # def submit_scrobble(self, scrobble):
  #   '''Send a Scrobble object to Last.fm to save a scrobble to a user\'s profile'''

  #   if not self.__is_logged_in():
  #     return

  #   scrobble_payload = {
  #     'method': 'track.scrobble',
  #     'track': scrobble.title,
  #     'artist': scrobble.artist.name,
  #     'timestamp': scrobble.timestamp.timestamp() # Convert from datetime object to UTC time
  #   }

  #   album_title = scrobble.album.title

  #   # Only submit album title if it exists
  #   if album_title:
  #     scrobble_payload['album'] = album_title

  #   return self.__lastfm_request(scrobble_payload, http_method='POST')

  # def set_track_is_loved(self, scrobble, is_loved):
  #   '''Set loved value on Last.fm for the passed scrobble'''

  #   if not self.__is_logged_in():
  #     return

  #   return self.__lastfm_request({
  #     'method': 'track.love' if is_loved else 'track.unlove',
  #     'track': scrobble.title,
  #     'artist': scrobble.artist.name
  #   }, http_method='POST')

  # def update_now_playing(self, scrobble):
  #   '''Tell Last.fm to update the user's now playing track'''

  #   if not self.__is_logged_in():
  #     return

  #   scrobble_payload = {
  #     'method': 'track.updateNowPlaying',
  #     'track': scrobble.title,
  #     'artist': scrobble.artist.name,
  #   }

  #   album_title = scrobble.album.title

  #   # Only submit album title if it exists
  #   if album_title:
  #     scrobble_payload['album'] = album_title

  #   return self.__lastfm_request(scrobble_payload, http_method='POST')

  # --- Other Methods ---

  def set_login_info(self, session_key, username):
    self.__session_key = session_key
    self.__username = username

  def generate_authorization_url(self, auth_token):
    '''Generate a Last.fm authentication url for the user to allow access to their account'''
    
    return f'https://www.last.fm/api/auth/?api_key={self.__api_key}&token={auth_token}'
  
  def get_total_scrobbles_today(self) -> int:
    # Get the unix timestamp of 12am today
    twelve_am_today = datetime.combine(datetime.now(), time.min).timestamp()

    return self.get_recent_scrobbles(
      limit=1, # We don't actually care about the tracks
      from_timestamp=int(twelve_am_today) # Trim decimal points per API requirement
    ).total

  # --- Private Methods ---

  def __lastfm_request(self, args, main_key_getter=None, return_value_builder=None, http_method='GET'):
    params = {
      'api_key': self.__api_key, 
      'format': 'json',
      **args
    }

    if http_method == 'POST':
      params['sk'] = self.__session_key

    params['api_sig'] = self.__generate_method_signature(params)

    # Make the request with automatic retries up to a limit
    for _ in range(LastfmApiWrapper.MAX_RETRIES):
      resp = requests.request(
        method=http_method,
        url='https://ws.audioscrobbler.com/2.0/', 
        headers={'user-agent': self.USER_AGENT},
        params=params if http_method == 'GET' else None,
        data=params if http_method == 'POST' else None
      )
      resp_json = None

      try:
        resp_json = resp.json()
      except json.decoder.JSONDecodeError:
        logger.critical(f'Last.fm returned non-JSON response: {resp.text}')
        return

      if 'error' in resp_json:
        # Ignore not found errors
        # TODO: Check for 404 code instead of error message
        if not resp_json['message'] in LastfmApiWrapper.NOT_FOUND_ERRORS:
          logger.error(f'Error requesting {args["method"]} response: {resp.text}')

      return_object = None
      
      try:
        if main_key_getter:
          return_object = return_value_builder(main_key_getter(resp_json), resp_json)
        else:
          return_object = return_value_builder(resp_json)
      except KeyError:
        # There's a missing key, run the request again by continuing the for loop
        continue

      # The object creation succeeded, so we can break out of the for loop and return
      return return_object
    else:
      # The for loop completed without breaking (The key was not found after the max number of retries)
      logger.critical(f'Could not request {method} after {LastfmApiWrapper.MAX_RETRIES} retries')
    
    return None

  def __generate_method_signature(self, payload):
    '''
    Create an api method signature from the request payload (in alphabetical order by key) with the client secret

    in: {'api_key': 'xxxxxxxxxx', 'method': 'auth.getSession', 'token': 'yyyyyyilovecher'}
    out: md5("api_keyxxxxxxxxxxmethodauth.getSessiontokenyyyyyyilovecher")
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
  
  @staticmethod
  def __tag_to_lastfm_tag(tag):
    return LastfmTag(
      name=tag['name'],
      url=tag['url']
    )

  # def get_auth_token(self):
  #   '''Request an authorization token used to get a the session key (lasts 60 minutes)'''
    
  #   return self.__lastfm_request('auth.getToken').get('token', '')

  # def get_session_key_and_username(self, auth_token):
  #   '''Use an auth token to get the session key and to access the user's account (does not expire)'''
    
  #   response_json = self.__lastfm_request({
  #     'method': 'auth.getSession',
  #     'token': auth_token
  #   })

  #   try:
  #     return response_json['session']['key'], response_json['session']['name']
  #   except KeyError:
  #     raise Exception(f'Error loading new session key: {response_json}')


















# Initialize api wrapper instance with login info once to use in multiple files
__lastfm_instance = None

def get_static_instance():
  global __lastfm_instance
  
  # If there isn't already LastfmApiWrapper instance, create one and log in using the saved credentials
  if not __lastfm_instance:
    __lastfm_instance = LastfmApiWrapper(os.environ['LASTREDUX_LASTFM_API_KEY'], os.environ['LASTREDUX_LASTFM_CLIENT_SECRET'])

    # Connect to SQLite
    db_helper.connect()

    # Set Last.fm wrapper session key and username from database
    session_key, username = db_helper.get_lastfm_session_details()
    __lastfm_instance.set_login_info(session_key, username)

  return __lastfm_instance