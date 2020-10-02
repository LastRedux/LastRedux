from datetime import date

from PySide2 import QtCore

from tasks.FetchProfileAndTopArtistsTask import FetchProfileAndTopArtistsTask
import util.LastfmApiWrapper as lastfm

class ProfileViewModel(QtCore.QObject):
  account_details_changed = QtCore.Signal()
  profile_statistics_changed = QtCore.Signal()
  top_artists_changed = QtCore.Signal()

  def __init__(self):
    QtCore.QObject.__init__(self)

    # Get instance of lastfm api wrapper
    self.lastfm_instance = lastfm.get_static_instance()

    self.account_details = None
    self.profile_statistics = None
    self.top_artists = None

  # --- Qt Property Getters ---

  def get_account_details(self):
    return self.account_details

  def get_profile_statistics(self):
    return self.profile_statistics
  
  def get_top_artists(self):
    import json
    return json.loads(json.dumps(self.top_artists, default=lambda o: o.__dict__))

  # --- Slots ---
  
  @QtCore.Slot()
  def loadProfileAndTopArtists(self):
    def __process_new_profile_and_top_artists(new_profile_statistics_and_top_artists):
      self.account_details = new_profile_statistics_and_top_artists['account_details']
      self.profile_statistics = new_profile_statistics_and_top_artists['profile_statistics']
      self.top_artists = new_profile_statistics_and_top_artists['top_artists']
      
      self.account_details_changed.emit()
      self.profile_statistics_changed.emit()
      self.top_artists_changed.emit()

    fetch_profile_and_top_artists_task = FetchProfileAndTopArtistsTask(self.lastfm_instance)
    fetch_profile_and_top_artists_task.finished.connect(__process_new_profile_and_top_artists)
    QtCore.QThreadPool.globalInstance().start(fetch_profile_and_top_artists_task)

  # --- Qt Properties ---

  accountDetails = QtCore.Property('QVariant', get_account_details, notify=account_details_changed)
  profileStatistics = QtCore.Property('QVariant', get_profile_statistics, notify=profile_statistics_changed)
  topArtists = QtCore.Property('QVariant', get_top_artists, notify=top_artists_changed)