from dataclasses import asdict
from util.spotify_api.SpotifyApiWrapper import SpotifyApiWrapper

from PySide2 import QtCore

from ApplicationViewModel import ApplicationViewModel
from tasks import FetchProfileStatistics
from datatypes import ProfileStatistics

class ProfileViewModel(QtCore.QObject):
  # Qt Property signals
  is_enabled_changed = QtCore.Signal()
  profile_statistics_changed = QtCore.Signal()
  should_show_loading_indicator_changed = QtCore.Signal()

  def __init__(self) -> None:
    QtCore.QObject.__init__(self)

    self.__application_reference: ApplicationViewModel = None
    self.__is_enabled: bool = False
    self.reset_state()

  def reset_state(self):
    self.__should_show_loading_indicator: bool = False

    self.__profile_statistics: ProfileStatistics = None
    self.__is_loading: bool = False

  # --- Slots ---
  
  @QtCore.Slot(bool)
  def loadProfile(self, was_app_refocused: bool=False) -> None:
    if not self.__is_enabled:
      return
    
    # Update loading indicator if needed
    if not self.__profile_statistics or was_app_refocused:
      self.__should_show_loading_indicator = True
      self.should_show_loading_indicator_changed.emit()

    # Don't reload if the profile page is already loading
    if self.__is_loading:
      return

    self.__is_loading = True

    # Clear data but don't update UI so that we can check later which parts have reloaded
    self.__user_info_top_artists = []
    self.__top_tracks = []
    self.__top_albums = []
    
    fetch_user_stats_top_artists_task = FetchProfileStatistics(
      lastfm=self.__application_reference.lastfm,
      spotify_api=self.__application_reference.spotify_api,
      album_art_provider=self.__application_reference.album_art_provider
    )
    fetch_user_stats_top_artists_task.finished.connect(self.__handle_user_statistics_top_artists_fetched)
    QtCore.QThreadPool.globalInstance().start(fetch_user_stats_top_artists_task)

    # fetch_top_tracks_task = FetchTopTracksTask(self.__application_reference.lastfm)
    # fetch_top_tracks_task.finished.connect(self.__handle_top_tracks_fetched)
    # QtCore.QThreadPool.globalInstance().start(fetch_top_tracks_task)
    
    # fetch_top_albums_task = FetchTopAlbumsTask(self.__application_reference.lastfm)
    # fetch_top_albums_task.finished.connect(self.__handle_top_albums_fetched)
    # QtCore.QThreadPool.globalInstance().start(fetch_top_albums_task)

  # --- Private Methods ---

  def __handle_user_statistics_top_artists_fetched(self, profile_statistics: ProfileStatistics):
    if not self.__is_enabled:
      return
    
    # Load profile statistics
    self.__profile_statistics = profile_statistics
    self.profile_statistics_changed.emit()

    # Update loading indicator
    self.__should_show_loading_indicator = False
    self.should_show_loading_indicator_changed.emit()
    self.__is_loading = False

  # --- Qt Property Getters and Setters ---

  def set_application_reference(self, new_reference: ApplicationViewModel) -> None:
    if not new_reference:
      return
    
    self.__application_reference = new_reference
    self.__application_reference.is_logged_in_changed.connect(
      lambda: self.set_is_enabled(self.__application_reference.is_logged_in)
    )

  def set_is_enabled(self, is_enabled: bool) -> None:
    self.__is_enabled = is_enabled
    self.is_enabled_changed.emit()
    self.reset_state()
    self.should_show_loading_indicator_changed.emit()

    if not is_enabled:
      self.profile_statistics_changed.emit()
      self.top_tracks_changed.emit()
      self.top_albums_changed.emit()

  # --- Qt Properties ---

  applicationReference = QtCore.Property(
    type=ApplicationViewModel,
    fget=lambda self: self.__application_reference,
    fset=set_application_reference
  )

  isEnabled = QtCore.Property(
    type=bool,
    fget=lambda self: self.__is_enabled, 
    fset=set_is_enabled, 
    notify=is_enabled_changed
  )

  profileStatistics = QtCore.Property(
    type='QVariant',
    fget=lambda self: asdict(self.__profile_statistics) if self.__profile_statistics else None,
    notify=profile_statistics_changed
  )

  shouldShowLoadingIndicator = QtCore.Property(
    type=bool,
    fget=lambda self: self.__should_show_loading_indicator,
    notify=should_show_loading_indicator_changed,
  )