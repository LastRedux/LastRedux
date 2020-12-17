import json

from loguru import logger
from PySide2 import QtCore

from tasks.FetchTopTracksTask import FetchTopTracksTask
from tasks.FetchTopAlbumsTask import FetchTopAlbumsTask
from tasks.FetchOverallStatsAndTopArtists import FetchOverallAndArtistStatistics
import util.LastfmApiWrapper as lastfm

class ProfileViewModel(QtCore.QObject):
  account_details_changed = QtCore.Signal()
  overall_statistics_changed = QtCore.Signal()
  top_artists_changed = QtCore.Signal()
  top_tracks_changed = QtCore.Signal()
  top_albums_changed = QtCore.Signal()
  should_show_loading_indicator_changed = QtCore.Signal()

  def __init__(self):
    QtCore.QObject.__init__(self)

    # Get instance of lastfm api wrapper
    self.lastfm_instance = lastfm.get_static_instance()

    self.__should_show_loading_indicator = False
    self.__account_details = None
    self.__overall_statistics = None
    self.__top_artists = None
    self.__top_tracks = None
    self.__top_albums = None
    self.__is_loading = False
  
  # --- Private Methods ---

  def __handle_loading_done(self):
    self.__should_show_loading_indicator = False
    self.should_show_loading_indicator_changed.emit()
    self.__is_loading = False
  
  def __process_new_profile_and_artist_statistics(self, new_overall_and_artist_statistics):
    logger.trace(f'Fetched Last.fm profile data and top artists for profile view')
    self.__account_details = new_overall_and_artist_statistics['account_details']
    self.__overall_statistics = new_overall_and_artist_statistics['overall_statistics']
    self.__top_artists = new_overall_and_artist_statistics['top_artists']
    
    self.account_details_changed.emit()
    self.overall_statistics_changed.emit()
    self.top_artists_changed.emit()

    # Update loading indicator on tab bar if it's showing and everythiing is loaded
    if self.__is_loading and self.__top_tracks and self.__top_albums:
      self.__handle_loading_done()

  def __process_new_top_albums(self, new_album_statistics):
    self.__top_albums = new_album_statistics
    self.top_albums_changed.emit()

    # Update loading indicator on tab bar if it's showing and everythiing is loaded
    if self.__is_loading and self.__top_tracks and self.__top_artists:
      self.__handle_loading_done()

  def __process_new_top_tracks(self, new_track_statistics):
    self.__top_tracks = new_track_statistics
    self.top_tracks_changed.emit()

    # Update loading indicator on tab bar if it's showing and everythiing is loaded
    if self.__is_loading and self.__top_albums and self.__top_artists:
      self.__handle_loading_done()

  # --- Slots ---
  
  @QtCore.Slot()
  @QtCore.Slot(bool)
  def loadProfileData(self, force_loading_indicator=False):
    # Enable loading indicator if initial load or window reactivated
    if not self.__overall_statistics or force_loading_indicator:
      self.__should_show_loading_indicator = True
      self.should_show_loading_indicator_changed.emit()

    if not self.__is_loading:
      self.__is_loading = True

      # Clear data but don't update UI so that we can check later which parts have reloaded
      self.__top_artists = []
      self.__top_tracks = []
      self.__top_albums = []
      
      # Load overall statistics and top artists
      fetch_overall_and_artist_statistics_task = FetchOverallAndArtistStatistics(self.lastfm_instance)
      fetch_overall_and_artist_statistics_task.finished.connect(self.__process_new_profile_and_artist_statistics)
      QtCore.QThreadPool.globalInstance().start(fetch_overall_and_artist_statistics_task)

      fetch_top_tracks_task = FetchTopTracksTask(self.lastfm_instance)
      fetch_top_tracks_task.finished.connect(self.__process_new_top_tracks)
      QtCore.QThreadPool.globalInstance().start(fetch_top_tracks_task)
      
      fetch_top_albums_task = FetchTopAlbumsTask(self.lastfm_instance)
      fetch_top_albums_task.finished.connect(self.__process_new_top_albums)
      QtCore.QThreadPool.globalInstance().start(fetch_top_albums_task)

  # --- Qt Properties ---

  # TODO: Simplify these account, profile, top artists to one property since they all load together
  accountDetails = QtCore.Property('QVariant', lambda self: self.__account_details, notify=account_details_changed)
  profileStatistics = QtCore.Property('QVariant', lambda self: self.__overall_statistics, notify=overall_statistics_changed)
  topArtists = QtCore.Property('QVariant', lambda self: json.loads(json.dumps(self.__top_artists, default=lambda o: o.__dict__)), notify=top_artists_changed)

  topTracks = QtCore.Property('QVariant', lambda self: json.loads(json.dumps(self.__top_tracks, default=lambda o: o.__dict__)), notify=top_tracks_changed)
  topAlbums = QtCore.Property('QVariant', lambda self: json.loads(json.dumps(self.__top_albums, default=lambda o: o.__dict__)), notify=top_albums_changed)

  shouldShowLoadingIndicator = QtCore.Property(bool, lambda self: self.__should_show_loading_indicator, notify=should_show_loading_indicator_changed)