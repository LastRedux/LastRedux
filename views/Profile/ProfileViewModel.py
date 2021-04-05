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
  is_loading_changed = QtCore.Signal()

  def __init__(self) -> None:
    QtCore.QObject.__init__(self)

    self._application_reference: ApplicationViewModel = None
    self._is_enabled: bool = False
    self.reset_state()

  def reset_state(self):
    self._profile_statistics: ProfileStatistics = None
    self._is_loading: bool = False

  # --- Slots ---
  
  @QtCore.Slot()
  def loadProfile(self) -> None:
    if not self._is_enabled:
      return

    if self._application_reference.is_offline:
      logging.debug('Offline, not loading profile')
      # Skip request if offline
      return

    # Don't reload if the profile page is already loading
    if self._is_loading:
      return

    self._is_loading = True
    self.is_loading_changed.emit()
    
    fetch_profile_statistics_task = FetchProfileStatistics(self._application_reference.lastfm,)
    fetch_profile_statistics_task.finished.connect(self._handle_profile_statistics_fetched)
    QtCore.QThreadPool.globalInstance().start(fetch_profile_statistics_task)

  # --- Private Methods ---

  def _handle_profile_statistics_fetched(
    self, 
    new_profile_statistics: ProfileStatistics
  ) -> None:
    if not self._is_enabled:
      return
    
    # Load new profile statistics if they changed (and there were some to begin with)
    if not self._profile_statistics or new_profile_statistics != self._profile_statistics:
      self._profile_statistics = new_profile_statistics
      self.profile_statistics_changed.emit()

      # Fetch Spotify artist images
      if self._profile_statistics.top_artists:
        load_profile_spotify_artists_task = LoadProfileSpotifyArtists(
          spotify_api=self._application_reference.spotify_api,
          top_artists=self._profile_statistics.top_artists
        )
        load_profile_spotify_artists_task.finished.connect(lambda: self.profile_statistics_changed.emit())
        QtCore.QThreadPool.globalInstance().start(load_profile_spotify_artists_task)

      if self._profile_statistics.top_artists_week:
        load_profile_spotify_artists_task = LoadProfileSpotifyArtists(
          spotify_api=self._application_reference.spotify_api,
          top_artists=self._profile_statistics.top_artists_week
        )
        load_profile_spotify_artists_task.finished.connect(lambda: self.profile_statistics_changed.emit())
        QtCore.QThreadPool.globalInstance().start(load_profile_spotify_artists_task)

    # Update loading indicator
    self._is_loading = False
    self.is_loading_changed.emit()

  # --- Qt Property Getters and Setters ---

  def set_application_reference(self, new_reference: ApplicationViewModel) -> None:
    if not new_reference:
      return
    
    self._application_reference = new_reference
    self._application_reference.is_logged_in_changed.connect(
      lambda: self.set_is_enabled(self._application_reference.is_logged_in)
    )

  def set_is_enabled(self, is_enabled: bool) -> None:
    self._is_enabled = is_enabled
    self.is_enabled_changed.emit()
    self.reset_state()
    self.is_loading_changed.emit()

    if not is_enabled:
      self.profile_statistics_changed.emit()
      self.top_tracks_changed.emit()
      self.top_albums_changed.emit()

  # --- Qt Properties ---

  applicationReference = QtCore.Property(
    type=ApplicationViewModel,
    fget=lambda self: self._application_reference,
    fset=set_application_reference
  )

  isEnabled = QtCore.Property(
    type=bool,
    fget=lambda self: self._is_enabled, 
    fset=set_is_enabled, 
    notify=is_enabled_changed
  )

  profileStatistics = QtCore.Property(
    type='QVariant',
    fget=lambda self: asdict(self._profile_statistics) if self._profile_statistics else None,
    notify=profile_statistics_changed
  )

  isLoading = QtCore.Property(
    type=bool,
    fget=lambda self: self._is_loading,
    notify=is_loading_changed,
  )