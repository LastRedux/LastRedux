from datetime import datetime

from datatypes.Track import Track
from datatypes.Artist import Artist
from datatypes.Album import Album
from datatypes.Tag import Tag
from datatypes.SimilarArtist import SimilarArtist
import util.LastfmApiWrapper as lastfm
import util.iTunesApiHelper as itunes_store

class Scrobble:
  lastfm_instance = None

  def __init__(self, track_title, artist_name, album_title=None, timestamp=None):
    '''Entry in scrobble history with track information and a timestamp'''

    # Create Track instance with associated Artist and Album instances
    artist = Artist(artist_name)
    album = Album(album_title)
    self.track = Track(track_title, artist, album)
    
    # Automatically generate timestamp if one isn't passed
    self.timestamp = timestamp or datetime.now()

    # All scrobbles should store a reference to the same lastfm api wrapper instance
    if not Scrobble.lastfm_instance:
      Scrobble.lastfm_instance = lastfm.get_static_instance()

  def load_lastfm_data(self):
    '''Request info from Last.fm about the track, album, and artist'''

    # Get track info from Last.fm
    track_response = Scrobble.lastfm_instance.get_track_info(self)
    self.track.has_requested_lastfm_data = True

    # Leave all attributes of the scrobble empty if the track is not in Last.fm's database
    if 'error' in track_response and track_response['message'] == 'Track not found':
      return

    self.track.load_lastfm_track_data(track_response['track'])
    self.track.artist.load_lastfm_artist_data(Scrobble.lastfm_instance.get_artist_info(self)['artist'])
    
    # Get album info from Last.fm if the track has an album
    if self.track.album.title:
      album_response = Scrobble.lastfm_instance.get_album_info(self)
      lastfm_album = album_response.get('album')
      
      # Not all tracks on Last.fm have an album (for example if a user scrobbles a track elsewhere and it shows up in history)
      if lastfm_album:
        self.track.album.load_lastfm_album_data(lastfm_album)

    self.track.has_lastfm_data = True
  
  def load_itunes_store_data(self):
    itunes_images = itunes_store.get_images(self.track.title, self.track.artist.name, self.track.album.title)

    if itunes_images:
      # Unpack itunes_images tuple
      artist_image, album_image_url, album_image_url_small = itunes_images

      self.track.artist.image_url = artist_image

      # Use iTunes album art if Last.fm didn't provide it
      if not self.track.album.image_url:
        self.track.album.image_url = album_image_url
        self.track.album.image_url_small = album_image_url_small

    self.track.has_itunes_store_data = True

  def equals(self, other_scrobble):
    '''Compare two scrobbles'''
    
    if not other_scrobble:
      return

    if self.track.has_lastfm_data and other_scrobble.track.has_lastfm_data:
      return self.track.lastfm_url == other_scrobble.track.lastfm_url
    
    return (
      self.track.title.lower() == other_scrobble.track.title.lower()
      and self.track.artist.name.lower() == other_scrobble.track.artist.name.lower()
      and self.track.album.title.lower() == other_scrobble.track.album.title.lower()
    )