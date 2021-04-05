import itertools
import logging
import os
from dataclasses import asdict
from datetime import datetime, timedelta
from typing import List

from PySide2 import QtCore

from tasks import UpdateTrackLoveOnLastfm, FetchRecentScrobbles
from util import db_helper
from util.lastfm import LastfmList, LastfmScrobble
from datatypes.Scrobble import Scrobble
from datatypes.MediaPlayerState import MediaPlayerState
from ApplicationViewModel import ApplicationViewModel

class HistoryViewModel(QtCore.QObject):
  # Constants
  _CURRENT_SCROBBLE_INDEX = -1
  _NO_SELECTION_INDEX = -2

  # Qt Property changed signals
  current_scrobble_data_changed = QtCore.Signal()
  selected_scrobble_changed = QtCore.Signal()
  selected_scrobble_index_changed = QtCore.Signal()
  is_loading_changed = QtCore.Signal()

  # List model signals
  pre_append_scrobble = QtCore.Signal()
  post_append_scrobble = QtCore.Signal()
  scrobble_album_image_changed = QtCore.Signal(int)
  scrobble_lastfm_is_loved_changed = QtCore.Signal(int)
  begin_refresh_history = QtCore.Signal()
  end_refresh_history = QtCore.Signal()

  def __init__(self) -> None:
    QtCore.QObject.__init__(self)

    self._application_reference: ApplicationViewModel = None
    self._scrobble_history: List[Scrobble] = None
    
    self._initialize_state()

  def _initialize_state(self) -> None:
    # Keep track of whether the history view is currently loading/reloading
    self._is_loading = False

    # Store currently playing track
    self._current_scrobble: Scrobble = None

    # Index of currently selected scrobble in history list
    self._selected_scrobble_index: int = None

    # Store Scrobble object at _selected_scrobble_index
    # This can either be a reference to the current scrobble or a scrobble object from history
    self.selected_scrobble: Scrobble = None


  # --- Qt Property Getters and Setters ---
  

  def set_application_reference(self, new_reference: ApplicationViewModel) -> None:
    if not new_reference:
      return
    
    self._application_reference = new_reference
    self._application_reference.is_logged_in_changed.connect(lambda: print('a'))

  def get_current_scrobble_data(self) -> dict:
    if not self._current_scrobble:
      return

    # Use dataclass.asdict to convert Scrobble object to a dict
    return asdict(self._current_scrobble)
  
  def get_selected_scrobble_index(self) -> int:
    if self._selected_scrobble_index is None:
      # NO_SELECTION_INDEX represents no selection because Qt doesn't understand Python's None value
      return self._NO_SELECTION_INDEX

    return self._selected_scrobble_index
  
  def set_selected_scrobble_index(self, new_index: int) -> None:
    # Prevent setting an illegal index value
    if (
      not self._application_reference.is_logged_in

      # Prevent navigating before current scrobble or past last scrobble
      or new_index < self._CURRENT_SCROBBLE_INDEX
      or new_index >= len(self._scrobble_history)

      # Prevent navigating to current scrobble if there isn't one
      or (
        new_index == self._CURRENT_SCROBBLE_INDEX
        and self._current_scrobble is None
      )
    ):
      return

    # Update selected scrobble index
    self._selected_scrobble_index = new_index
    self.selected_scrobble_index_changed.emit()

    # Update selected scrobble
    if new_index == self._CURRENT_SCROBBLE_INDEX:
      self.selected_scrobble = self._current_scrobble
    else:
      self.selected_scrobble = self._scrobble_history[new_index]

    # Update details view with new selected scrobble
    self.selected_scrobble_changed.emit()


  # --- Slots ---


  @QtCore.Slot()
  def reloadHistory(self) -> None:
    '''Load recent scrobbles from Last.fm'''

    if (
      self._application_reference.preferences['initial_history_length'] == 0
      
      # Prevent reloading during onboarding/logging out
      or not self._application_reference.is_logged_in

      # Prevent reloading while the view is already loading
      or self._is_loading
    ):
      return

    # Update loading indicator
    self._is_loading = True
    self.is_loading_changed.emit()

    # Reset scrobble history
    self.begin_refresh_history.emit()
    self._scrobble_history = []
    self.end_refresh_history.emit()

    # Fetch and load recent scrobbles
    fetch_recent_scrobbles_task = FetchRecentScrobbles(
      lastfm=self._application_reference.lastfm, 
      count=self._application_reference.preferences['initial_history_length']
    )
    fetch_recent_scrobbles_task.finished.connect(self._handle_recent_scrobbles_fetched)
    QtCore.QThreadPool.globalInstance().start(fetch_recent_scrobbles_task)
  
  @QtCore.Slot(int)
  def toggleLastfmIsLoved(self, scrobble_index: int) -> None:
    if not self._application_reference.is_logged_in:
      return

    scrobble = None

    # Find scrobble by index
    if scrobble_index == self._CURRENT_SCROBBLE_INDEX:
      scrobble = self._current_scrobble
    else:
      scrobble = self._scrobble_history[scrobble_index]

    new_is_loved = not scrobble.lastfm_track.is_loved

    # Update is_loved in memory
    scrobble.lastfm_track.is_loved = new_is_loved

    # Update any matching scrobbles in either current scrobble or scrobble history
    for _scrobble in itertools.chain(self._current_scrobble, self._scrobble_history):
      if _scrobble == scrobble:
        _scrobble.lastfm_track.is_loved = new_is_loved

    # Update UI to reflect changes
    self._emit_scrobble_ui_update_signals(scrobble)

    # Submit new is_loved value to Last.fm
    QtCore.QThreadPool.globalInstance().start(
      UpdateTrackLoveOnLastfm(
        lastfm=self._application_reference.lastfm,
        scrobble=scrobble,
        value=new_is_loved
      )
    )
  

  # --- Private Methods ---


  def _emit_scrobble_ui_update_signals(self, scrobble: Scrobble) -> None:
    if not self._application_reference.is_logged_in:
      return
    
    # Update details view if needed (all external scrobble data)
    if scrobble == self.selected_scrobble:
      self.selected_scrobble_changed.emit()
    
    # Update current scrobble view if needed (album art, is_loved)
    if scrobble == self._current_scrobble:
      self.current_scrobble_data_changed.emit()
    
    # Update is_loved and album art for applicable history items if they match
    for i, _scrobble in enumerate(self._scrobble_history):
      if _scrobble == scrobble:
        self.scrobble_album_image_changed.emit(i)
        self.scrobble_lastfm_is_loved_changed.emit(i)

  def _handle_recent_scrobbles_fetched(self, recent_scrobbles: LastfmList[LastfmScrobble]) -> None:
    self.begin_refresh_history.emit()

    # User might not have any scrobbles (new account)
    if recent_scrobbles:
      # Convert scrobbles from history into Scrobble objects
      for _scrobble in recent_scrobbles.items:
        self._scrobble_history.append(
          Scrobble.from_lastfm_scrobble(_scrobble)
        )

        self._load_external_scrobble_data(_scrobble)

    self.end_refresh_history.emit()

    # Update is_loading
    self._is_loading = False
    self.is_loading_changed.emit()


  # --- Qt Properties ---


  applicationReference = QtCore.Property(
    type=ApplicationViewModel,
    fget=lambda self: self._application_reference,
    fset=set_application_reference
  )

  currentScrobbleData = QtCore.Property(
    type='QVariant',
    fget=get_current_scrobble_data,
    notify=current_scrobble_data_changed
  )

  selectedScrobbleIndex = QtCore.Property(
    type=int,
    fget=get_selected_scrobble_index,
    fset=set_selected_scrobble_index,
    notify=selected_scrobble_index_changed
  )

  isLoading = QtCore.Property(
    type=bool,
    fget=lambda self: self._is_loading,
    notify=is_loading_changed
  )