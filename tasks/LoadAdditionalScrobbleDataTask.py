from PySide2 import QtCore

from models.Scrobble import Scrobble

class LoadAdditionalScrobbleDataTask(QtCore.QObject, QtCore.QRunnable):
  emit_scrobble_ui_update_signals = QtCore.Signal(Scrobble)
  finished = QtCore.Signal()

  def __init__(self, scrobble: Scrobble, should_load_itunes_store_data, is_part_of_initial_batch=False):
    QtCore.QObject.__init__(self)
    QtCore.QRunnable.__init__(self)

    self.scrobble = scrobble
    self.should_load_itunes_store_data = should_load_itunes_store_data
    self.is_part_of_initial_batch = is_part_of_initial_batch
    self.setAutoDelete(True)

  def run(self):
    '''Fetch and attach information from Last.fm and iTunes to the passed Scrobble object and emit signals to update that specific scrobble in the UI'''

    # Refresh details view with Last.fm details if it doesn't exist
    if not self.scrobble.has_lastfm_data:
      self.scrobble.load_lastfm_data()
      self.emit_scrobble_ui_update_signals.emit(self.scrobble)

    # Don't load iTunes data for tracks that are being loaded from Last.fm as recent tracks or tracks that already have iTunes data
    if not self.should_load_itunes_store_data or self.scrobble.has_itunes_store_data:
      if self.is_part_of_initial_batch:
        self.finished.emit()
      
      return

    # Get artist image and album art from iTunes
    self.scrobble.load_itunes_store_data()
    self.emit_scrobble_ui_update_signals.emit(self.scrobble)

    if self.is_part_of_initial_batch:
      self.finished.emit()