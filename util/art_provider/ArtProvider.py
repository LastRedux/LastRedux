from util.spotify_api.SpotifyArtist import SpotifyArtist
from loguru import logger

from util.lastfm import LastfmApiWrapper
from util.spotify_api import SpotifyApiWrapper
from datatypes.ImageSet import ImageSet
import util.itunes_store_api_helper as itunes_store
from .ScrobbleImages import ScrobbleImages

class ArtProvider:
  def __init__(self, lastfm: LastfmApiWrapper, spotify_api: SpotifyApiWrapper):
    self.lastfm = lastfm
    self.spotify_api = spotify_api

  def get_album_art(self, artist_name: str, track_title: str, album_title: str=None) -> ImageSet:
    '''Get album art from whichever source can find it'''

    album_art = ImageSet(None, None)

    # 1. Try geting album art from Last.fm if there's an album title to work with
    if album_title:
      album_art = self.__get_lastfm_album_art(artist_name, album_title)

    if not album_art:
      # 2. Try geting album art from the Spotify api (doesn't need an album title, has more art)
      album_art = self.spotify_api.get_track_images(
        artist_name,
        track_title,
        album_title,
        only_album_art=True # We don't want artist images
      ).album_art

      if not album_art:
        # 3. Try geting album art from the iTunes Store api
        album_art = itunes_store.get_album_art(artist_name, track_title, album_title)

    return album_art

  def get_scrobble_images(
    self,
    artist_name: str,
    track_title: str,
    album_title: str=None
  ) -> ScrobbleImages:
    '''Get Spotify artist images and album art'''

    # 1. Try getting artist images and album art from Spotify
    spotify_data = self.spotify_api.get_track_images(artist_name, track_title, album_title)
    
    # 2. Try getting album art from Last.fm (we prefer Last.fm art to Spotify art if it exists)
    album_art = self.__get_lastfm_album_art(artist_name, album_title)

    if not album_art:
      if spotify_data.album_art:
        # 3. Use Spotify album art if there is any
        album_art = spotify_data.album_art
      else:
        # 4. Try getting art from the iTunes Store api
        album_art = itunes_store.get_album_art(artist_name, track_title, album_title)

    return ScrobbleImages(album_art, spotify_data.artists)

  # --- Private Methods ---

  def __get_lastfm_album_art(self, artist_name: str, album_title: str) -> ImageSet:
    '''Get an album's artwork from Last.fm'''

    album_info = self.lastfm.get_album_info(artist_name, album_title)

    if not album_info:
      return

    if album_info.image_set:
      return album_info.image_set

    if ' - Single' in album_title:
      album_info = self.lastfm.get_album_info(artist_name, album_title.replace(' - Single', ''))

      if album_info:
        # Some albums don't exist yet on Last.fm

        if album_info.image_set:
          return album_info.image_set

    return None