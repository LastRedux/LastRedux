from __future__ import annotations # For self-referential return type
from dataclasses import dataclass, field
from typing import List, ClassVar

from loguru import logger

import util.LastfmApiWrapper as lastfm
from util.LastfmApiWrapper import LastfmApiWrapper
import util.spotify_api_helper as spotify_api_helper
from datatypes.Artist import Artist
from datatypes.SpotifyArtist import SpotifyArtist
from datatypes.Album import Album
from datatypes.Tag import Tag

@dataclass
class Track:
  title: str
  artist: Artist
  album: Album

  # Reference to helper instances
  lastfm_instance: ClassVar[LastfmApiWrapper] = lastfm.get_static_instance()

  # Last.fm data
  lastfm_url: str = ''
  lastfm_global_listeners: int = 0
  lastfm_global_plays: int = 0
  lastfm_plays: int = 0
  lastfm_is_loved: bool = False
  lastfm_tags: List[Tag] = field(default_factory=list)

  # Spotify data
  spotify_artists: List[SpotifyArtist] = field(default_factory=list)

  # Loading state
  has_requested_lastfm_data: bool = False
  has_lastfm_data: bool = False
  has_spotify_data: bool = False

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

    # Load track info if there isn't already some loaded (ie. Friends page)
    if not self.lastfm_url:
      lastfm_track_sucessfully_loaded = False

      while not lastfm_track_sucessfully_loaded:        
        # Get track info from Last.fm
        track_response = Track.lastfm_instance.get_track_info(self)
        self.has_requested_lastfm_data = True

        # Leave all attributes of the track empty if the track is not in Last.fm's database
        if 'error' in track_response and track_response['message'] == 'Track not found':
          return

        try:
          # Load non-image attributes of the Last.fm track.getInfo response
          self.load_lastfm_track_data(track_response['track'])
          lastfm_track_sucessfully_loaded = True
        except KeyError as e:
          # There is a missing key in the Last.fm response
          logger.warning(f'Last.fm returned an incomplete track response: {self.title} - {e}')

    # Load artist info from Last.fm if there isn't already some some loaded (ie. Friends page)
    if not self.artist.lastfm_url:
      self.artist.load_lastfm_artist_data(Track.lastfm_instance.get_artist_info(self)['artist'])

    # Load album data from Last.fm if the track has an album
    if self.album.title:
      lastfm_album = Track.lastfm_instance.get_album_info(self.artist.name, self.album.title).get('album')
      
      # Load album url even if there isn't an image in the response
      if lastfm_album:
        self.album.load_lastfm_album_data(lastfm_album)

        # Only log successful album art load if album art was actually loaded (Last.fm can return blank strings for image urls even when the album exists)
        if self.album.image_url:
          logger.debug(f'Album art found on Last.fm: {self.title} | {self.album.title}')
    
    # Try getting an album without ' - Single' if there is an album title
    if not self.album.image_url and self.album.title:
      album_title_no_single = self.album.title.replace(' - Single', '')

      # Only try getting non-single album art for tracks with album titles that have - Single in their name
      if album_title_no_single != self.album.title:
        lastfm_album_no_single = Track.lastfm_instance.get_album_info(self.artist.name, album_title_no_single).get('album')
      
        # Load album art if there is an image in the response (Last.fm can return blank strings for image urls even when the album exists)
        if lastfm_album_no_single and lastfm_album_no_single['image'][0].get('#text', ''):
          # Only load images, not album url since it isn't technically the right album
          self.album.load_lastfm_images(lastfm_album_no_single['image'])
          logger.debug(f'Album art found on Last.fm (single label removed): {self.title} | {self.album.title}')

    # If all previous methods to find album art fail, use track art instead (usually a 'single' album art ie. `Aamon - Single`)
    # One of the following could result in this case: 
    # - The track has no album data
    # - The album doesn't exist on Last.fm 
    # - The album on Last.fm has no image
    if not self.album.image_url:
      # Request a track.getInfo response since we didn't request it earlier (most likely we are on the friends page)
      if not track_response:
        track_response = Track.lastfm_instance.get_track_info(self)

      if track_response.get('image'):
        self.album.load_lastfm_track_images(track_response['image'])
        logger.debug(f'Album art found on Last.fm (track image): {self.title} | {self.album.title}')

    self.has_lastfm_data = True
  
  def load_spotify_data(self):
    spotify_images = spotify_api_helper.get_images(self.title, self.artist.name, self.album.title)

    if spotify_images:
      artists, album_image, album_image_small = spotify_images
      self.spotify_artists = artists

      # Use Spotify album art if Last.fm didn't provide it
      if not self.album.image_url:
        self.album.image_url = album_image
        self.album.image_url_small = album_image_small
        logger.debug(f'Album art found on Spotify: {self.title} | {self.album.title}')

    self.has_spotify_data = True

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