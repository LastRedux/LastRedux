from datetime import datetime

from datatypes.Track import Track
from datatypes.Artist import Artist
from datatypes.Album import Album
from datatypes.Tag import Tag
from datatypes.SimilarArtist import SimilarArtist
import util.LastfmApiWrapper as lastfm
import util.iTunesApiHelper as itunes_store

class Scrobble:
  lastfm = None

  def __init__(self, track_title, artist_name, album_name, timestamp=None):
    '''Entry in scrobble history with track information and a timestamp'''

    # Create Track instance with associated Artist and Album instances
    artist = Artist(artist_name)
    album = Album(album_name)
    self.track = Track(track_title, artist, album)
    
    # Automatically generated timestamp
    self.timestamp = datetime.now()

    # All scrobbles should store a reference to the same lastfm api wrapper instance
    if not Scrobble.lastfm:
      Scrobble.lastfm = lastfm.get_static_instance()

  def load_lastfm_data(self):
    '''Request info from Last.fm about the track, album, and artist'''

    # Get track info from Last.fm
    track_response = Scrobble.lastfm.get_track_info(self)

    if not track_response:
      return

    lastfm_track = track_response['track']
    self.track.lastfm_url = lastfm_track['url']
    self.track.lastfm_global_listeners = int(lastfm_track['listeners'])
    self.track.lastfm_global_plays = int(lastfm_track['playcount'])
    self.track.lastfm_plays = int(lastfm_track['userplaycount'])
    self.track.lastfm_is_loved = bool(int(lastfm_track['userloved'])) # Convert 0/1 to bool
    self.track.lastfm_tags = list(map(lambda tag: Tag(tag['name'], tag['url']), lastfm_track['toptags']['tag']))

    # Get artist info from Last.fm
    lastfm_artist = Scrobble.lastfm.get_artist_info(self)['artist']
    self.track.artist.lastfm_url = lastfm_artist['url']
    self.track.artist.lastfm_global_listeners = int(lastfm_artist['stats']['listeners'])
    self.track.artist.lastfm_global_plays = int(lastfm_artist['stats']['playcount'])
    self.track.artist.lastfm_plays = int(lastfm_artist['stats']['userplaycount'])
    self.track.artist.bio = lastfm_artist['bio']['content'].split(' <')[0].strip() # Remove read more on Last.fm link because a QML Link component is used instead
    self.track.artist.lastfm_tags = list(map(lambda tag: Tag(tag['name'], tag['url']), lastfm_artist['tags']['tag']))
    self.track.artist.lastfm_similar_artists = list(map(lambda similar_artist: SimilarArtist(similar_artist['name'], similar_artist['url']), lastfm_artist['similar']['artist']))
    
    # Get album info from Last.fm
    lastfm_album = Scrobble.lastfm.get_album_info(self)['album']
    self.track.album.lastfm_url = lastfm_album['url']
    self.track.album.lastfm_plays = int(lastfm_album['userplaycount'])
    self.track.album.image_url = lastfm_album['image'][4]['#text'] # Pick mega size in images array
    self.track.album.image_url_small = lastfm_album['image'][1]['#text'] # Pick medium size in images array

    self.track.has_lastfm_data = True
  
  def load_itunes_store_data(self):
    artist_image, album_image_url, album_image_url_small = itunes_store.get_images(self.track.title, self.track.artist.name, self.track.album.title)

    self.track.artist.image_url = artist_image

    # Use iTunes album art if Last.fm didn't provide it
    if not self.track.album.image_url:
      self.track.album.image_url = album_image_url
      self.track.album.image_url_small = album_image_url_small

    self.track.has_itunes_store_data = True