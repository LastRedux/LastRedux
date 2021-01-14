from dataclasses import asdict
import json
from datetime import datetime

from PySide2 import QtCore

from HistoryViewModel import HistoryViewModel

class DetailsViewModel(QtCore.QObject):
  # Qt Property changed signals
  scrobble_changed = QtCore.Signal()
  is_in_mini_mode_changed = QtCore.Signal()
  is_player_paused_changed = QtCore.Signal()
  media_player_name_changed = QtCore.Signal()

  def __init__(self) -> None:
    QtCore.QObject.__init__(self)

    # Store a reference to the scrobble history view model instance that provides data
    self.__history_reference: HistoryViewModel = None

    # Store whether the app is in mini mode
    self.__is_in_mini_mode: bool = None

  # --- Qt Property Getters and Setters ---

  def set_history_reference(self, new_reference: HistoryViewModel) -> None:
    if not new_reference:
      return

    self.__history_reference = new_reference

    # Pass through signals from history view model
    self.__history_reference.selected_scrobble_changed.connect(
      lambda: self.scrobble_changed.emit()
    )
    self.__history_reference.is_player_paused_changed.connect(
      lambda: self.is_player_paused_changed.emit()
    )
    self.__history_reference.media_player_name_changed.connect(
      lambda: self.media_player_name_changed.emit()
    )

    # Update details view immediately after connecting
    self.scrobble_changed.emit()
    self.media_player_name_changed.emit()

  # --- Slots ---

  @QtCore.Slot()
  def toggleMiniMode(self) -> None:
    if not self.__is_enabled:
      return

    self.__is_in_mini_mode = not self.__is_in_mini_mode
    self.is_in_mini_mode_changed.emit()

  # --- Qt Properties ---

  historyReference = QtCore.Property(
    HistoryViewModel, lambda self: self.__history_reference, set_history_reference
  )

  scrobble = QtCore.Property(
    type='QVariant',
    fget=lambda self: (
      asdict(self.__history_reference.selected_scrobble)
      if self.__history_reference.selected_scrobble else None
    ) if self.__history_reference else None,
    notify=scrobble_changed
  )

  isCurrentScrobble = QtCore.Property(
    type=bool,
    fget=lambda self: (
      self.__history_reference.get_selected_scrobble_index() == -1
      if self.__history_reference else None
    ),
    notify=scrobble_changed
  )

  isInMiniMode = QtCore.Property(
    type=bool,
    fget=lambda self: self.__is_in_mini_mode,
    notify=is_in_mini_mode_changed
  )

  isPlayerPaused = QtCore.Property(
    type=bool,
    fget=lambda self: (
      self.__history_reference.is_player_paused
      if self.__history_reference else None
    ),
    notify=is_player_paused_changed
  )

  mediaPlayerName = QtCore.Property(
    type=str,
    fget=lambda self: (
      str(self.__history_reference.media_player) 
      if self.__history_reference else None
    ),
    notify=media_player_name_changed
  )