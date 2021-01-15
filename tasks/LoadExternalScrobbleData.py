from datatypes import ProfileStatistic
from PySide2 import QtCore

from util.lastfm import LastfmApiWrapper, LastfmUser
from util.art_provider import ArtProvider
from datatypes.Scrobble import Scrobble

class LoadExternalScrobbleData(QtCore.QObject, QtCore.QRunnable):
  update_ui_for_scrobble = QtCore.Signal(Scrobble)
  finished = QtCore.Signal()

  def __init__(self, lastfm: LastfmApiWrapper, art_provider: ArtProvider, scrobble: Scrobble):
    QtCore.QObject.__init__(self)
    QtCore.QRunnable.__init__(self)
    self.lastfm = lastfm
    self.art_provider = art_provider
    self.scrobble = scrobble
    self.setAutoDelete(True)

  def run(self):
    '''Load Last.fm track + artist info, album art for scrobble and update the UI progressively'''

    # 1. Fetch and load Last.fm track info (first becuase we need is_loved value)
    self.scrobble.lastfm_track = self.lastfm.get_track_info(
      artist_name=self.scrobble.artist_name,
      track_title=self.scrobble.track_title
    )
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

    # 3. Fetch Last.fm artist info if a track was found on Last.fm
    if self.scrobble.lastfm_track:
      self.scrobble.lastfm_track.artist = self.lastfm.get_artist_info(self.scrobble.artist_name)
      self.update_ui_for_scrobble.emit(self.scrobble)

      # 4. Fetch Last.fm album info
      self.scrobble.lastfm_track.album = self.lastfm.get_album_info(
        artist_name=self.scrobble.artist_name,
        album_title=self.scrobble.album_title
      )
      self.scrobble.is_loading = False
      self.update_ui_for_scrobble.emit(self.scrobble)

      # # 4. Load friend artist leaderboard
      # def __generate_statistic(user: LastfmUser, plays: int) -> ProfileStatistic:
      #   return ProfileStatistic(
      #     title=user.username,
      #     plays=plays,
      #     image_url=user.image_url,
      #     lastfm_url=user.url
      #   )
      
      # friends = self.lastfm.get_friends()
      # artist_leaderboard = []
      # # track_leaderboard = []

      # # Add logged in user to friends to list in the leaderboard
      # # TODO: Request cached data
      # friends.append(self.lastfm.get_user_info())

      # for user in friends:
      #   artist_info = self.lastfm.get_artist_info(self.scrobble.lastfm_track.artist.name, user.username)
      #   # track_info = self.lastfm.get_track_info(self.scrobble.lastfm_track.artist.name, self.scrobble.lastfm_track.title, user.username)

      #   if artist_info.plays:
      #     artist_leaderboard.append(__generate_statistic(user, artist_info.plays))
        
      #   # if track_info.plays:
      #   #   track_leaderboard.append(__generate_statistic(user, track_info.plays))

      # self.scrobble.friend_artist_leaderboard = sorted(
      #   artist_leaderboard, 
      #   key=lambda stat: stat.plays,
      #   reverse=True
      # )

      # highest = self.scrobble.friend_artist_leaderboard[0].plays

      # for stat in self.scrobble.friend_artist_leaderboard:
      #   stat.percentage = stat.plays / highest

      # track_leaderboard = sorted(track_leaderboard, key=lambda stat: stat.plays, reverse=True)

      # self.update_ui_for_scrobble.emit()

    self.finished.emit()