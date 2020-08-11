import time
import json
import hashlib
import webbrowser
import requests

class LastFmApiWrapper:
  USER_AGENT = 'LastRedux v0.0.0'

  def __init__(self, api_key, client_secret):
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

  def __lastfm_request(self, payload, http_method='GET'):
    '''Make an HTTP request to last.fm and attach the needed keys'''
    
    headers = {'user-agent': self.USER_AGENT}

    payload['api_key'] = self.__api_key
    payload['format'] = 'json'

    if self.__session_key:
      payload['sk'] = self.__session_key

    # Generate method signature after all other keys are added to the payload
    payload['api_sig'] = self.__generate_method_signature(payload)

    if http_method == 'GET':
      return requests.get('http://ws.audioscrobbler.com/2.0/', headers=headers, params=payload).json()
    elif http_method == 'POST':
      return requests.post('http://ws.audioscrobbler.com/2.0/', headers=headers, data=payload).json()
    else:
      raise Exception('Invalid HTTP method') 

  def __is_logged_in(self):
    if not self.__session_key or not self.__username:
      raise Exception('Last.fm api wrapper not logged in')
    
    return True

  def get_auth_token(self):
    '''Request an authorization token used to get a the session key (lasts 60 minutes)'''
    
    return self.__lastfm_request({
      'method': 'auth.getToken'
    })['token']

  def set_login_info(self, session_key, username):
    self.__session_key = session_key
    self.__username = username

  def open_authorization_url(self, auth_token):
    '''Launch default browser to allow user to authorize our app'''
    
    webbrowser.open(f'http://www.last.fm/api/auth/?api_key={self.__api_key}&token={auth_token}')

  def get_new_session(self, auth_token):
    '''Use an auth token to get a session key to access the user's account (does not expire)'''
    
    response_json = self.__lastfm_request({
      'method': 'auth.getSession',
      'token': auth_token
    })

    try:
      session_data = response_json['session']

      return {
        'session_key': session_data['key'],
        'username': session_data['name']
      }
    except KeyError:
      print(response_json)

  def get_track_info(self, scrobble):
    '''Get track info about a Scrobble object from a user's Last.fm library'''
    
    if not self.__is_logged_in():
      return 

    return self.__lastfm_request({
      'method': 'track.getInfo',
      'track': scrobble.track['name'],
      'artist': scrobble.track['artist']['name'],
      'username': self.__username,
      'timestamp': scrobble.timestamp.timestamp() # Convert from datetime object to UTC time
    })

  def get_album_info(self, scrobble):
    '''Get album info about a Scrobble object from a user's Last.fm library'''
    
    if not self.__is_logged_in():
      return 

    return self.__lastfm_request({
      'method': 'album.getInfo',
      'artist': scrobble.track['artist']['name'],
      'album': scrobble.track['album']['name'],
      'username': self.__username,
      'timestamp': scrobble.timestamp.timestamp() # Convert from datetime object to UTC time
    })

  def get_artist_info(self, scrobble):
    '''Get artist info about a Scrobble object from a user's Last.fm library'''

    if not self.__is_logged_in():
      return 

    return self.__lastfm_request({
      'method': 'artist.getInfo',
      'artist': scrobble.track['artist']['name'],
      'username': self.__username,
      'timestamp': scrobble.timestamp.timestamp() # Convert from datetime object to UTC time
    })

  def submit_scrobble(self, scrobble):
    '''Send a Scrobble object to Last.fm to save a scrobble to a user\'s profile'''

    if not self.__is_logged_in():
      return 

    return self.__lastfm_request({
      'method': 'track.scrobble',
      'track': scrobble.track['name'],
      'artist': scrobble.track['artist']['name'],
      'album': scrobble.track['album']['name'],
      'timestamp': scrobble.timestamp.timestamp() # Convert from datetime object to UTC time
    }, http_method='POST')