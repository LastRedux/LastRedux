import re

import requests

class SpotifyWebApiHelper:
  def __init__(self, CLIENT_ID, CLIENT_SECRET):
    self.CLIENT_ID = CLIENT_ID
    self.CLIENT_SECRET = CLIENT_SECRET
    self.token = ''

  def log_in(self, token=''):
    if token:
      self.token = token
      return token

    resp = requests.post('https://accounts.spotify.com/api/token', data={
    'grant_type': 'client_credentials'
    }, auth=(self.CLIENT_ID, self.CLIENT_SECRET))

    token = resp.json()['access_token']
    self.token = token
    return token

  def get_images(self, track_title, artist_name, album_title):
    print(f'Requesting images for "{artist_name} {track_title} {album_title}""')

    stripped_track_title = re.sub(r'[^A-za-z0-9 ]+', '', track_title)
    stripped_track_title = stripped_track_title.replace('feat', '')
    # stripped_album_title = re.sub(r'[^A-za-z0-9\- ]+', '', album_title)

    resp = requests.get('https://api.spotify.com/v1/search', params={
      'q': f'{artist_name} {stripped_track_title}',
      'type': 'track'
    }, headers={
      'Accept': 'application/json',
      'Authorization': f'Bearer {self.token}'
    })

    track_json = resp.json()

    track = track_json['tracks']['items'][0]

    print(f'Found track: {track["name"]}')
    album_images = track['album']['images']
    print(f'Found album: {track["album"]["name"]}')

    album_image = album_images[0]['url']
    album_image_small = album_images[-1]['url']
    artist_ids = [artist['id'] for artist in track['artists']]
    artists = []

    for artist_id in artist_ids:
      artist_resp = requests.get(f'https://api.spotify.com/v1/artists/{artist_id}', headers={
        'Accept': 'application/json',
        'Authorization': f'Bearer {self.token}'
      })

      artist_json = artist_resp.json()
      artist_name = artist_json['name']
      artist_image = artist_json['images'] and artist_json['images'][-1]['url']

      artists.append((artist_name, artist_image))

    return artists, album_image, album_image_small