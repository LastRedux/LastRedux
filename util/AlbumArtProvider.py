from loguru import logger

from util.lastfm import LastfmApiWrapper
from util.spotify_api import SpotifyApiWrapper
from datatypes.ImageSet import ImageSet
import util.itunes_store_api_helper as itunes_store

class AlbumArtProvider:
  def __init__(self, lastfm: LastfmApiWrapper, spotify_api: SpotifyApiWrapper):
    self.lastfm = lastfm
    self.spotify_api = spotify_api

  def get_album_art(self, artist_name: str, track_title: str, album_title: str=None) -> ImageSet:
    # 1. Try geting album art from Last.fm
    album_art = self.get_lastfm_album_art(artist_name, album_title)

    if album_art:
      logger.trace(f'Found album art for {track_title} on Last.fm')
    else:
      # 2. Try geting album art from the Spotify api
      album_art = self.spotify_api.get_images(artist_name, track_title, album_title)

      if album_art:
        logger.trace(f'Found album art for {track_title} on Spotify')
      else:
        # 3. Try geting album art from the iTunes Store api
        album_art = itunes_store.get_album_art(artist_name, track_title, album_title)
        
        if album_art:
          logger.trace(f'Found album art for {track_title} on the iTunes Store')

    return album_art

  def get_lastfm_album_art(self, artist_name: str, album_title: str) -> ImageSet:
    '''Get an album's artwork from Last.fm'''

    album_info = self.lastfm.get_album_info(artist_name, album_title)

    if album_info.image_set:
      return album_info.image_set

    if ' - Single' in album_title:
      album_info = self.lastfm.get_album_info(artist_name, album_title.replace(' - Single', ''))

      if album_info:
        # Some albums don't exist yet on Last.fm

        if album_info.image_set:
          return album_info.image_set

    return None