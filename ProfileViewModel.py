import logging
from dataclasses import asdict

from PySide2 import QtCore

from ApplicationViewModel import ApplicationViewModel
from datatypes.ProfileStatistics import ProfileStatistics
from tasks import FetchProfileStatistics, LoadProfileSpotifyArtists

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

    if self.__application_reference.is_offline:
      logging.debug('Offline, not loading profile')
      # Skip request if offline
      return
    
    # Update loading indicator if needed
    # if not self.__profile_statistics or was_app_refocused:
    self.__should_show_loading_indicator = True
    self.should_show_loading_indicator_changed.emit()

    # Don't reload if the profile page is already loading
    if self.__is_loading:
      return

    self.__is_loading = True
    
    fetch_profile_statistics_task = FetchProfileStatistics(self.__application_reference.lastfm,)
    fetch_profile_statistics_task.finished.connect(self.__handle_profile_statistics_fetched)
    QtCore.QThreadPool.globalInstance().start(fetch_profile_statistics_task)

  # --- Private Methods ---

  def __handle_profile_statistics_fetched(
    self, 
    new_profile_statistics: ProfileStatistics
  ) -> None:
    if not self.__is_enabled:
      return
    
    # Load new profile statistics if they changed (and there were some to begin with)
    if not self.__profile_statistics or new_profile_statistics != self.__profile_statistics:
      self.__profile_statistics = new_profile_statistics

      # Fetch Spotify artist images
      load_profile_spotify_artists_task = LoadProfileSpotifyArtists(
        spotify_api=self.__application_reference.spotify_api,
        top_artists=(
          # Concatenate both lists since we're passing by reference and we want to load all together
          self.__profile_statistics.top_artists + self.__profile_statistics.top_artists_week
        )
      )
      load_profile_spotify_artists_task.finished.connect(lambda: self.profile_statistics_changed.emit())
      QtCore.QThreadPool.globalInstance().start(load_profile_spotify_artists_task)

    # Update loading indicator
    self.__is_loading = False
    self.__should_show_loading_indicator = False
    self.should_show_loading_indicator_changed.emit()

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