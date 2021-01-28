from datatypes.ProfileStatistic import ProfileStatistic
import logging

from PySide2 import QtCore

from util.lastfm import LastfmApiWrapper, LastfmUser
from util.art_provider import ArtProvider
from datatypes.Scrobble import Scrobble

class LoadExternalScrobbleData(QtCore.QObject, QtCore.QRunnable):
  update_ui_for_scrobble = QtCore.Signal(Scrobble)
  finished = QtCore.Signal()

  def __init__(self, lastfm: LastfmApiWrapper, art_provider: ArtProvider, scrobble: Scrobble, should_load_leaderboard: bool=False):
    QtCore.QObject.__init__(self)
    QtCore.QRunnable.__init__(self)
    self.lastfm = lastfm
    self.art_provider = art_provider
    self.scrobble = scrobble
    self.should_load_leaderboard = should_load_leaderboard
    self.setAutoDelete(True)

  def run(self):
    '''Load Last.fm track + artist info, album art for scrobble and update the UI progressively'''

    # 1. Fetch and load Last.fm track info (first becuase we need is_loved value)
    lastfm_track = None
    
    try:
      lastfm_track = self.lastfm.get_track_info(
        artist_name=self.scrobble.artist_name,
        track_title=self.scrobble.track_title
      )
    except Exception as err:
      self.scrobble.has_error = True
      logging.error(err)

    self.scrobble.lastfm_track = lastfm_track # Could be None
    self.update_ui_for_scrobble.emit(self.scrobble)

    # 2. Fetch album art and artist images
    scrobble_images = self.art_provider.get_scrobble_images(
      artist_name=self.scrobble.artist_name,
      track_title=self.scrobble.track_title,
      album_title=self.scrobble.album_title
    )
    self.scrobble.image_set = scrobble_images.album_art
    self.scrobble.spotify_artists = scrobble_images.spotify_artists
    self.update_ui_for_scrobble.emit(self.scrobble)

    # 3. Fetch Last.fm artist info
    self.scrobble.lastfm_artist = self.lastfm.get_artist_info(self.scrobble.artist_name)
    self.update_ui_for_scrobble.emit(self.scrobble)

    # 4. Fetch Last.fm album info
    self.scrobble.lastfm_album = self.lastfm.get_album_info(
      artist_name=self.scrobble.artist_name,
      album_title=self.scrobble.album_title
    )
    self.update_ui_for_scrobble.emit(self.scrobble)

    self.scrobble.is_loading = False

    # 5. Fetch artist and track leaderboards
    if self.should_load_leaderboard:      
      friends = self.lastfm.get_friends()
      artist_leaderboard = []

      # Add logged in user to friends to list in the leaderboard
      # TODO: Request cached data
      friends.append(self.lastfm.get_user_info())

      for user in friends:
        artist_info = self.lastfm.get_artist_info(self.scrobble.lastfm_artist.name, user.username)

        if artist_info.plays:
          artist_leaderboard.append(ProfileStatistic(
            title=user.username,
            plays=artist_info.plays,
            image_url=user.image_url,
            lastfm_url=user.url
          ))

      artist_leaderboard = sorted(
        artist_leaderboard, 
        key=lambda stat: stat.plays,
        reverse=True
      )

      highest = artist_leaderboard[0].plays

      for stat in artist_leaderboard:
        stat.percentage = stat.plays / highest

      self.scrobble.friend_artist_leaderboard = artist_leaderboard
      self.update_ui_for_scrobble.emit(self.scrobble)
    
    self.finished.emit()