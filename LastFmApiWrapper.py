import time
import json
import hashlib
import webbrowser
import requests

class LastFmApiWrapper:
  USER_AGENT = 'LastRedux v0.0.0'

  def __init__(self, api_key, client_secret):
    self.api_key = api_key
    self.client_secret = client_secret
    self.session_key = None

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
    param = ''.join(param) + self.client_secret

    # Unicode encode param before hashing
    param = param.encode()

    # Attach the api signature to the payload
    api_sig = hashlib.md5(param).hexdigest()
    
    return api_sig

  def __lastfm_request(self, payload, http_method='GET'):
    '''Make an HTTP request to last.fm and attach the needed keys'''
    
    headers = {'user-agent': self.USER_AGENT}

    payload['api_key'] = self.api_key
    payload['format'] = 'json'

    if self.session_key:
      payload['sk'] = self.session_key

    # Generate method signature after all other keys are added to the payload
    payload['api_sig'] = self.__generate_method_signature(payload)

    if http_method == 'GET':
      return requests.get('http://ws.audioscrobbler.com/2.0/', headers=headers, params=payload).json()
    elif http_method == 'POST':
      return requests.post('http://ws.audioscrobbler.com/2.0/', headers=headers, data=payload).json()
    else:
      raise Exception('Invalid HTTP method') 

  def get_auth_token(self):
    '''Request an authorization token used to get a the session key (lasts 60 minutes)'''
    
    return self.__lastfm_request({
      'method': 'auth.getToken'
    })['token']

  def open_authorization_url(self, auth_token):
    '''Launch default browser to allow user to authorize our app'''
    
    webbrowser.open(f'http://www.last.fm/api/auth/?api_key={self.api_key}&token={auth_token}')

  def get_new_session_key(self, auth_token):
    '''Use an auth token to get a session key to access the user's account (does not expire)'''
    
    response_json = self.__lastfm_request({
      'method': 'auth.getSession',
      'token': auth_token
    })

    try:
      session_key = response_json['session']['key']
      self.session_key = session_key

      return session_key
    except KeyError:
      print(response_json)

  def submit_scrobble(self, scrobble):
    '''Send a Scrobble object to Last.fm to save a scrobble to a user\'s profile'''
    return self.__lastfm_request({
      'method': 'track.scrobble',
      'track': scrobble.track,
      'artist': scrobble.artist,
      'album': scrobble.album,
      'timestamp': scrobble.timestamp.timestamp() # Convert from datetime object to UTC time
    }, http_method='POST')