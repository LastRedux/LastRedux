from __future__ import annotations # For self-referential return type

from dataclasses import dataclass, field
from typing import List, ClassVar

import util.LastfmApiWrapper as lastfm
import util.spotify_api_helper as spotify_api_helper
from datatypes.Artist import Artist
from datatypes.SpotifyArtist import SpotifyArtist
from datatypes.Album import Album
from datatypes.SimilarArtist import SimilarArtist
from datatypes.Tag import Tag

@dataclass
class Track:
  title: str
  artist: Artist
  album: Album

  # Reference to helper instances
  lastfm_instance: ClassVar = lastfm.get_static_instance()

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
      lastfm_album = Track.lastfm_instance.get_album_info(self.artist.name, self.album.title).get('album')
      
      # If the album exists on Last.fm
      if lastfm_album:
        self.album.load_lastfm_album_data(lastfm_album)
    
    # No matter what, if no album art was found, use track art instead (usually a 'single' album art ie. `Aamon - Single`)
    # One of the following cases: 
    # - The track has no album data
    # - The album doesn't exist on Last.fm 
    # - The album on Last.fm has no image
    if not self.album.image_url:
      # Try getting an album without ' - Single' if there is an album title
      if self.album.title:
        album_title_no_single = self.album.title.replace(' - Single', '')

        # Only try getting non-single album art for tracks with album titles that have - Single in their name
        if album_title_no_single != self.album.title:
          lastfm_album_no_single = Track.lastfm_instance.get_album_info(self.artist.name, album_title_no_single).get('album')
        
          if lastfm_album_no_single:
            self.album.load_lastfm_album_data(lastfm_album_no_single)
            self.has_lastfm_data = True
            return

      # Try getting "canonical" album images
      # Request a track.getInfo response since we didn't request it earlier (most likely we are on the friends page)
      if not track_response:
        track_response = Track.lastfm_instance.get_track_info(self)

      if track_response.get('image'):
        self.album.load_lastfm_track_images(track_response['image'])

    self.has_lastfm_data = True
  
  def load_spotify_data(self):
    spotify_images = spotify_api_helper.get_images(self.title, self.artist.name, self.album.title)

    if spotify_images:
      artists, album_image, album_image_small = spotify_images
      self.spotify_artists = artists

      self.artist.image_url = self.spotify_artists[0].image_url

      # Use Spotify album art if Last.fm didn't provide it
      if not self.album.image_url:
        self.album.image_url = album_image
        self.album.image_url_small = album_image

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