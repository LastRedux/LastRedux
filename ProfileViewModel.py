import json

from loguru import logger
from PySide2 import QtCore

from tasks.FetchProfileAndTopArtistsTask import FetchProfileAndTopArtistsTask
import util.LastfmApiWrapper as lastfm

class ProfileViewModel(QtCore.QObject):
  account_details_changed = QtCore.Signal()
  profile_statistics_changed = QtCore.Signal()
  top_artists_changed = QtCore.Signal()
  should_show_loading_indicator_changed = QtCore.Signal()

  def __init__(self):
    QtCore.QObject.__init__(self)

    # Get instance of lastfm api wrapper
    self.lastfm_instance = lastfm.get_static_instance()

    self.__should_show_loading_indicator = False
    self.__account_details = None
    self.__profile_statistics = None
    self.__top_artists = None
    self.__is_loading = False

  # --- Slots ---
  
  @QtCore.Slot()
  @QtCore.Slot(bool)
  def loadProfileAndTopArtists(self, force_loading_indicator=False):
    def __process_new_profile_and_top_artists(new_profile_statistics_and_top_artists):
      logger.trace(f'Fetched Last.fm profile data and top artists for profile view')
      self.__account_details = new_profile_statistics_and_top_artists['account_details']
      self.__profile_statistics = new_profile_statistics_and_top_artists['profile_statistics']
      self.__top_artists = new_profile_statistics_and_top_artists['top_artists']
      
      self.account_details_changed.emit()
      self.profile_statistics_changed.emit()
      self.top_artists_changed.emit()

      # Update loading indicator on tab bar if needed
      if self.__should_show_loading_indicator:
        self.__should_show_loading_indicator = False
        self.should_show_loading_indicator_changed.emit()

      self.__is_loading = False

    # Enable loading indicator if initial load or window reactivated
    if not self.__profile_statistics or force_loading_indicator:
      self.__should_show_loading_indicator = True
      self.should_show_loading_indicator_changed.emit()

    if not self.__is_loading:
      self.__is_loading = True
      
      fetch_profile_and_top_artists_task = FetchProfileAndTopArtistsTask(self.lastfm_instance)
      fetch_profile_and_top_artists_task.finished.connect(__process_new_profile_and_top_artists)
      QtCore.QThreadPool.globalInstance().start(fetch_profile_and_top_artists_task)

  # --- Qt Properties ---

  accountDetails = QtCore.Property('QVariant', lambda self: self.__account_details, notify=account_details_changed)
  profileStatistics = QtCore.Property('QVariant', lambda self: self.__profile_statistics, notify=profile_statistics_changed)
  topArtists = QtCore.Property('QVariant', lambda self: json.loads(json.dumps(self.__top_artists, default=lambda o: o.__dict__)), notify=top_artists_changed)
  shouldShowLoadingIndicator = QtCore.Property(bool, lambda self: self.__should_show_loading_indicator, notify=should_show_loading_indicator_changed)