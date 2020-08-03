from PySide2 import QtCore

from ScrobbleHistoryViewModel import *

class ScrobbleDetailsViewModel(QtCore.QObject):
  scrobble_data_changed = QtCore.Signal()

  def __init__(self):
    QtCore.QObject.__init__(self)

    # Store a reference to the scrobble history view model instance that provides data
    self.__scrobble_history_reference = None

  # --- Qt Property Getters and Setters ---

  def get_scrobble_history_reference(self):
    return self.__scrobble_history_reference

  def set_scrobble_history_reference(self, new_reference):
    # Only change the view model reference if there is a new one (don't reload when closing the app)
    if new_reference:
      self.__scrobble_history_reference = new_reference

      # Connect to scrobble selection change on view model, so when a new scrobble is selected, details will update
      self.__scrobble_history_reference.selected_scrobble_changed.connect(lambda: self.scrobble_data_changed.emit())

      # Update scrobble data because the scrobble data changed signal won't be triggered upon connection
      self.scrobble_data_changed.emit()

  def get_scrobble_data(self):
    if self.__scrobble_history_reference and self.__scrobble_history_reference.selected_scrobble:
        return self.__scrobble_history_reference.selected_scrobble.track
    
    return None

  # --- Qt Properties ---

  # Allow the __scrobble_history_reference to be set in the view
  scrobbleHistoryReference = QtCore.Property(ScrobbleHistoryViewModel, get_scrobble_history_reference, set_scrobble_history_reference)

  # Make the __scrobble_history_reference available to the view
  scrobbleData = QtCore.Property('QVariant', get_scrobble_data, notify=scrobble_data_changed)