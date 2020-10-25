import json

from loguru import logger
from PySide2 import QtCore

from tasks.FetchProfileAndTopArtistsTask import FetchProfileAndTopArtistsTask
import util.LastfmApiWrapper as lastfm

class ProfileViewModel(QtCore.QObject):
  account_details_changed = QtCore.Signal()
  profile_statistics_changed = QtCore.Signal()
  top_artists_changed = QtCore.Signal()
  is_loading_changed = QtCore.Signal()

  def __init__(self):
    QtCore.QObject.__init__(self)

    # Get instance of lastfm api wrapper
    self.lastfm_instance = lastfm.get_static_instance()

    self.__is_loading = False
    self.__account_details = None
    self.__profile_statistics = None
    self.__top_artists = None

  # --- Slots ---
  
  @QtCore.Slot()
  def loadProfileAndTopArtists(self):
    def __process_new_profile_and_top_artists(new_profile_statistics_and_top_artists):
      logger.trace(f'Fetched Last.fm profile data and top artists for profile view')
      self.__account_details = new_profile_statistics_and_top_artists['account_details']
      self.__profile_statistics = new_profile_statistics_and_top_artists['profile_statistics']
      self.__top_artists = new_profile_statistics_and_top_artists['top_artists']
      
      self.account_details_changed.emit()
      self.profile_statistics_changed.emit()
      self.top_artists_changed.emit()

      # Update loading indicator on tab bar
      self.__is_loading = False
      self.is_loading_changed.emit()

    # Update loading indicator on tab bar
    self.__is_loading = True
    self.is_loading_changed.emit()

    fetch_profile_and_top_artists_task = FetchProfileAndTopArtistsTask(self.lastfm_instance)
    fetch_profile_and_top_artists_task.finished.connect(__process_new_profile_and_top_artists)
    QtCore.QThreadPool.globalInstance().start(fetch_profile_and_top_artists_task)

  # --- Qt Properties ---

  accountDetails = QtCore.Property('QVariant', lambda self: self.__account_details, notify=account_details_changed)
  profileStatistics = QtCore.Property('QVariant', lambda self: self.__profile_statistics, notify=profile_statistics_changed)
  topArtists = QtCore.Property('QVariant', lambda self: json.loads(json.dumps(self.__top_artists, default=lambda o: o.__dict__)), notify=top_artists_changed)
  isLoading = QtCore.Property(bool, lambda self: self.__is_loading, notify=is_loading_changed)