from dataclasses import asdict

from PySide2 import QtCore

from ..History.HistoryViewModel import HistoryViewModel
from ApplicationViewModel import ApplicationViewModel

class DetailsViewModel(QtCore.QObject):
  # Qt Property changed signals
  scrobble_changed = QtCore.Signal()
  is_player_paused_changed = QtCore.Signal()
  media_player_name_changed = QtCore.Signal()
  is_offline_changed = QtCore.Signal()

  def __init__(self) -> None:
    QtCore.QObject.__init__(self)

    # Store a reference to the scrobble history view model instance that provides data
    self._history_reference: HistoryViewModel = None

    # Store a reference to the application view model
    self._application_reference: ApplicationViewModel = None

  # --- Qt Property Getters and Setters ---

  def set_history_reference(self, new_reference: HistoryViewModel) -> None:
    if not new_reference:
      return

    self._history_reference = new_reference

    # Pass through signals from history view model
    self._history_reference.selected_scrobble_changed.connect(
      lambda: self.scrobble_changed.emit()
    )
    self._history_reference.is_player_paused_changed.connect(
      lambda: self.is_player_paused_changed.emit()
    )
    self._history_reference.media_player_name_changed.connect(
      lambda: self.media_player_name_changed.emit()
    )

    # Update details view immediately after connecting
    self.scrobble_changed.emit()
    self.media_player_name_changed.emit()

  def set_application_reference(self, new_reference: ApplicationViewModel) -> None:
    if not new_reference:
      return

    self._application_reference = new_reference

    # Pass through signal from application view model
    self._application_reference.is_offline_changed.connect(
      lambda: self.is_offline_changed.emit()
    )

  # --- Qt Properties ---

  applicationReference = QtCore.Property(
    type=ApplicationViewModel,
    fget=lambda self: self._application_reference,
    fset=set_application_reference
  )

  historyReference = QtCore.Property(
    type=HistoryViewModel,
    fget=lambda self: self._history_reference,
    fset=set_history_reference
  )

  scrobble = QtCore.Property(
    type='QVariant',
    fget=lambda self: (
      asdict(self._history_reference.selected_scrobble)
      if self._history_reference.selected_scrobble else None
    ) if self._history_reference else None,
    notify=scrobble_changed
  )

  isCurrentScrobble = QtCore.Property(
    type=bool,
    fget=lambda self: (
      self._history_reference.get_selected_scrobble_index() == -1
      if self._history_reference else None
    ),
    notify=scrobble_changed
  )

  isOffline = QtCore.Property(
    type=bool,
    fget=(
      lambda self: self._application_reference.is_offline
      if self._application_reference else None
    ),
    notify=is_offline_changed
  )

  isPlayerPaused = QtCore.Property(
    type=bool,
    fget=lambda self: (
      self._history_reference.is_player_paused
      if self._history_reference else None
    ),
    notify=is_player_paused_changed
  )

  mediaPlayerName = QtCore.Property(
    type=str,
    fget=lambda self: (
      self._history_reference.mediaPlayerName
      if self._history_reference else None
    ),
    notify=media_player_name_changed
  )