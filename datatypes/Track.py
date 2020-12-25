from __future__ import annotations # For self-referential return type
from dataclasses import dataclass, field
from typing import List, ClassVar

from loguru import logger

import util.LastfmApiWrapper as lastfm
from util.LastfmApiWrapper import LastfmApiWrapper
import util.spotify_api_helper as spotify_api_helper
import util.itunes_store_api_helper as itunes_store_api_helper
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
  
  # Possible values:
  # - INITIALIZED: Just media player data
  # - LASTFM_TRACK_LOADED: Has loaded info from Last.fm
  # - LASTFM_TRACK_NOT_FOUND: Track isn't on Last.fm
  loading_state: str = 'INITIALIZED'

  def load_lastfm_track_object(self, lastfm_track) -> None:
    '''Load a Last.fm track.getInfo response into the Track schema'''

    self.lastfm_url = lastfm_track['url']
    self.lastfm_global_listeners = int(lastfm_track['listeners'])
    self.lastfm_global_plays = int(lastfm_track['playcount'])
    self.lastfm_plays = int(lastfm_track['userplaycount'])
    self.lastfm_is_loved = bool(int(lastfm_track['userloved'])) # Convert 0/1 to bool
    self.lastfm_tags = list(map(lambda tag: Tag(tag['name'], tag['url']), lastfm_track['toptags']['tag']))

  @staticmethod
  def build_from_lastfm_recent_track(lastfm_recent_track) -> Track:
    '''Build a Track from a user scrobble event (does NOT contain user plays nor global stats)'''

    album_title = lastfm_recent_track.get('album').get('#text')

    return Track(
      lastfm_recent_track['name'],
      Artist(
        lastfm_recent_track['artist']['name'],
        lastfm_url=lastfm_recent_track['artist']['url']
      ),
      # Some Last.fm tracks don't have albums associated with them
      Album(
        album_title,
        lastfm_url=lastfm_recent_track.get('album').get('url')
      ),
      lastfm_url=lastfm_recent_track['url']
    )
  
  def fetch_and_load_lastfm_track_data(self):
    '''Fetch and load track data from a Last.fm track.getInfo response'''

    track_response = Track.lastfm_instance.get_track_info(self)
    logger.trace(f'{self.title}: Fetched Last.fm track data')
    self.has_requested_lastfm_data = True

    if 'error' in track_response:
      if track_response['message'] == 'Track not found':
        logger.trace(f'{self.title}: Track not found on Last.fm')
        self.loading_state = 'LASTFM_TRACK_NOT_FOUND'
      else:
        logger.error(f'{self.title}: Last.fm track.getInfo returned an error `{track_response}`')
  
      return

    try:
      # Load non-image attributes of the Last.fm track.getInfo response
      self.load_lastfm_track_object(track_response['track'])
    except KeyError as e:
      # There is a missing key in the Last.fm response
      logger.trace(f'{self.title}: Last.fm returned an incomplete track response `{repr(e)}`')

      # Retry requesting track data from Last.fm, usually if there's a missing key, retrying the request will resolve the issue
      self.fetch_and_load_lastfm_track_data()
  
    # Return the track response because we may use it later
    return track_response

  def fetch_and_load_lastfm_artist_data(self):
    '''Fetch and load track data from a Last.fm artist.getInfo response'''

    artist_response = Track.lastfm_instance.get_artist_info(self)
    logger.trace(f'{self.title}: Fetched Last.fm artist data for `{self.artist.name}`')

    if 'error' in artist_response:
      if artist_response['message'] == 'The artist you supplied could not be found':
        logger.trace(f'{self.title}: Artist not found on Last.fm')
      else:
        logger.error(f'{self.title}: Last.fm artist.getInfo for `{self.artist.name}` returned an error {artist_response}')
  
      return

    try:
      self.artist.load_lastfm_artist_object(artist_response['artist'])
    except KeyError as e:
      # There is a missing key in the Last.fm response
      logger.trace(f'{self.title}: Last.fm returned an incomplete artist response `{repr(e)}`')

      # Retry requesting artist data from Last.fm, usually if there's a missing key, retrying the request will resolve the issue
      self.fetch_and_load_lastfm_artist_data()

  def fetch_and_load_lastfm_album_data(self, album_title, is_fallback=False):
    '''Fetch and load album data from a Last.fm album.getInfo response'''

    album_response = Track.lastfm_instance.get_album_info(self.artist.name, album_title)
    logger.trace(f'{self.title}: Fetched Last.fm album data for `{album_title}`')

    if 'error' in album_response:
      # Don't log error if a fallback album (with ` - Single ` removed) doesn't exist on Last.fm
      if album_response['message'] == 'Album not found':
        if not is_fallback:
          logger.trace(f'{self.title}: Album not found on Last.fm')    
      else:
        logger.error(f'{self.title}: Last.fm album.getInfo for `{album_title}` returned an error {album_response}')

      return

    try:
      self.album.load_lastfm_album_object(album_response['album'], only_images=is_fallback)
    except KeyError as e:
      # There is a missing key in the Last.fm response
      logger.trace(f'{self.title}: Last.fm returned an incomplete album response `{repr(e)}`')

      # Retry requesting album data from Last.fm, usually if there's a missing key, retrying the request will resolve the issue
      self.fetch_and_load_lastfm_album_data(album_title)
  
  def fetch_and_load_spotify_data(self, search_without_album=False, no_artists=False) -> bool:
    spotify_images = None
    
    if search_without_album:
      spotify_images = spotify_api_helper.get_images(self.title, self.artist.name, '', no_artists=no_artists)
      logger.trace(f'{self.title}: Fetched Spotify search data (album title excluded)')
    else:
      spotify_images = spotify_api_helper.get_images(self.title, self.artist.name, self.album.title, no_artists=no_artists)
      logger.trace(f'{self.title}: Fetched Spotify search data')

    if spotify_images:
      artists, album_image, album_image_small = spotify_images
      self.spotify_artists = artists

      # Use Spotify album art if Last.fm didn't provide it
      if self.album.title and not self.album.image_url:
        self.album.image_url = album_image
        self.album.image_url_small = album_image_small
        logger.trace(f'{self.title}: Album art found on Spotify')

  def fetch_and_load_itunes_store_images(self):
    itunes_images = None

    if self.album.title:
      itunes_images = itunes_store_api_helper.get_images(self.title, self.artist.name, self.album.title)
    else:
      itunes_images = itunes_store_api_helper.get_images(self.title, self.artist.name)

    logger.trace(f'{self.title}: Fetched iTunes Store search data')

    if itunes_images:
      album_image, album_image_small = itunes_images

      self.album.image_url = album_image
      self.album.image_url_small = album_image_small
      logger.trace(f'{self.title}: Album art found on iTunes search')

  def load_lastfm_data(self, no_artists=False):
    '''Fill in data about the track, album, and artist from Last.fm'''

    track_response = None

    # Load track and artist info unless there is already some loaded (ie. Friends page)
    if not no_artists:
      track_response = self.fetch_and_load_lastfm_track_data()
      self.fetch_and_load_lastfm_artist_data()

    # Load album info from Last.fm if the track has an album
    if self.album.title:
      self.fetch_and_load_lastfm_album_data(self.album.title)
      
      if self.album.image_url:
        logger.trace(f'{self.title}: Album art found on Last.fm')
      else:
        # Try fetching album art for the album name without ` - Single` (Some music services do not label singles)
        if ' - Single' in self.album.title:
          self.fetch_and_load_lastfm_album_data(self.album.title.replace(' - Single', ''), is_fallback=True)
          
        if self.album.image_url:
          logger.trace(f'{self.title}: Album art found on Last.fm (album with single label removed)')

      # Use track art instead (usually a 'single' album art ie. `Aamon - Single`)
      # One of the following could result in this case: 
    # One of the following could result in this case: 
      # One of the following could result in this case: 
    # One of the following could result in this case: 
      # One of the following could result in this case: 
      # - The track has no album data
      # - The album doesn't exist on Last.fm
      # - The album on Last.fm has no image
      if not self.album.image_url:
        # Request a track.getInfo response if we didn't already (Such as on the friends page where additional track and artist info isn't needed)
        if not track_response:
          track_response = Track.lastfm_instance.get_track_info(self)

        # Not all tracks have an image associated with them
        if 'image' in track_response:
          self.album.load_lastfm_track_images(track_response['image'])
          logger.trace(f'{self.title}: Album art found on Last.fm (track image)')
  
    if not self.loading_state == 'LASTFM_TRACK_NOT_FOUND':
      self.loading_state = 'LASTFM_TRACK_LOADED'

  def load_spotify_data(self, no_artists=False):
    if self.album.title:
      self.fetch_and_load_spotify_data(no_artists=no_artists)
      
      # Retry Spotify search without album title if search failed
      if not len(self.spotify_artists):
        # Try again without the album (better chance of a match)
        spotify_images_loaded = self.fetch_and_load_spotify_data(search_without_album=True, no_artists=no_artists)

        if spotify_images_loaded:
          logger.trace(f'{self.title}: Album art found on Spotify (album title excluded from search)')
    else:
      # Always search without album if there isn't one associated with the scrobble
      self.fetch_and_load_spotify_data(search_without_album=True, no_artists=no_artists)

  def load_itunes_store_images(self):
    # Try getting album art from iTunes as a last resort
    if not self.album.image_url:
      self.fetch_and_load_itunes_store_images()

  def equals(self, other_track: Track):
    '''Compare two tracks'''
    
    if not other_track:
      return

    if self.loading_state == 'LASTFM_LOADED' and other_track.loading_state == 'LASTFM_LOADED':
      return self.lastfm_url == other_track.lastfm_url
    
    # Default to a blank string if there are no album titles
    album_title = self.album.title or ''
    other_album_title = other_track.album.title or ''

    return (
      self.title.lower() == other_track.title.lower()
      and self.artist.name.lower() == other_track.artist.name.lower()
      and album_title.lower() == other_album_title.lower()
    )