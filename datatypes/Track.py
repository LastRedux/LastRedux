from __future__ import annotations # For self-referential return type

from dataclasses import dataclass, field
from typing import List, ClassVar

import util.iTunesApiHelper as itunes_store
import util.LastfmApiWrapper as lastfm
from datatypes.Artist import Artist
from datatypes.Album import Album
from datatypes.SimilarArtist import SimilarArtist
from datatypes.Tag import Tag

@dataclass
class Track:
  # Media player data
  title: str
  artist: Artist
  album: Album

  # Reference to Last.fm instance
  lastfm_instance: ClassVar = lastfm.get_static_instance()

  # Last.fm data
  lastfm_url: str = ''
  lastfm_global_listeners: int = 0
  lastfm_global_plays: int = 0
  lastfm_plays: int = 0
  lastfm_is_loved: bool = False
  lastfm_tags: List[Tag] = field(default_factory=list)

  # Loading state
  has_requested_lastfm_data: bool = False
  has_lastfm_data: bool = False
  has_itunes_store_data: bool = False

  def load_lastfm_track_data(self, lastfm_track) -> None:
    self.lastfm_url = lastfm_track['url']
    self.lastfm_global_listeners = int(lastfm_track['listeners'])
    self.lastfm_global_plays = int(lastfm_track['playcount'])
    self.lastfm_plays = int(lastfm_track['userplaycount'])
    self.lastfm_is_loved = bool(int(lastfm_track['userloved'])) # Convert 0/1 to bool
    self.lastfm_tags = list(map(lambda tag: Tag(tag['name'], tag['url']), lastfm_track['toptags']['tag']))

  @staticmethod
  def build_from_lastfm_recent_track(lastfm_recent_track) -> Track:
    '''Build a Track from a user scrobble event (does NOT contain user plays nor global stats)'''

    return Track(
      lastfm_recent_track['name'], 
      Artist(lastfm_recent_track['artist']['name'], lastfm_url=lastfm_recent_track['artist']['url']), 
      Album(lastfm_recent_track.get('album').get('#text'), lastfm_url=lastfm_recent_track.get('album').get('url')), # Some Last.fm tracks don't have albums associated with them
      lastfm_url=lastfm_recent_track['url']
    )

  def load_lastfm_data(self):
    '''Fill in data about the track, album, and artist from Last.fm'''

    track_response = None

    # Don't load track info if there is already some loaded (Friends page)
    if not self.lastfm_url:
      # Get track info from Last.fm
      track_response = Track.lastfm_instance.get_track_info(self)
      self.has_requested_lastfm_data = True

      # Leave all attributes of the track empty if the track is not in Last.fm's database
      if 'error' in track_response and track_response['message'] == 'Track not found':
        return

      lastfm_track = track_response['track']
      self.load_lastfm_track_data(lastfm_track)

    # Don't load artist info if there is already some loaded (Friends page)
    if not self.artist.lastfm_url:
      self.artist.load_lastfm_artist_data(Track.lastfm_instance.get_artist_info(self)['artist'])

    # If the track has album data
    if self.album.title:
      lastfm_album = Track.lastfm_instance.get_album_info(self).get('album')
      
      # If the album exists on Last.fm
      if lastfm_album:
        self.album.load_lastfm_album_data(lastfm_album)
    
    # No matter what, if no album art was found, use track art instead (usually a 'single' album art ie. `Aamon - Single`)
    # One of the following cases: 
    # - The track has no album data
    # - The album doesn't exist on Last.fm 
    # - The album on Last.fm has no image
    if not self.album.image_url:
      if not track_response:
        # Request a track.getInfo response since we didn't request it earlier (most likely we are on the friends page)
        track_response = Track.lastfm_instance.get_track_info(self)

      if track_response.get('image'):
        self.album.load_lastfm_track_images(track_response['image'])

    self.has_lastfm_data = True
  
  def load_itunes_store_data(self):
    itunes_images = itunes_store.get_images(self.title, self.artist.name, self.album.title)

    if itunes_images:
      # Unpack itunes_images tuple
      artist_image, album_image_url, album_image_url_small = itunes_images

      # self.artist.image_url = artist_image

      # Use iTunes album art if Last.fm didn't provide it
      if not self.album.image_url:
        self.album.image_url = album_image_url
        self.album.image_url_small = album_image_url_small

    self.has_itunes_store_data = True

  def equals(self, other_track: Track):
    '''Compare two tracks'''
    
    if not other_track:
      return

    if self.has_lastfm_data and other_track.has_lastfm_data:
      return self.lastfm_url == other_track.lastfm_url
    
    return (
      self.title.lower() == other_track.title.lower()
      and self.artist.name.lower() == other_track.artist.name.lower()
      and self.album.title.lower() == other_track.album.title.lower()
    )