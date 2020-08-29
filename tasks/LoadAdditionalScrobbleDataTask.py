from PySide2 import QtCore

from models.Scrobble import Scrobble

class LoadAdditionalScrobbleDataTask(QtCore.QObject, QtCore.QRunnable):
  emit_scrobble_ui_update_signals = QtCore.Signal(Scrobble)

  def __init__(self, scrobble):
    QtCore.QObject.__init__(self)
    QtCore.QRunnable.__init__(self)
    self.scrobble = scrobble
    self.setAutoDelete(True)

  def run(self):
    '''Fetch and attach information from Last.fm to the __current_scrobble Scrobble object and emit signals to update that specific scrobble in the UI'''

    # Refresh details view with Last.fm details if it doesn't exist
    if not self.scrobble.track.has_lastfm_data:
      self.scrobble.load_lastfm_data()
      self.emit_scrobble_ui_update_signals.emit(self.scrobble)
    
    # Get artist image and album art from iTunes
    if not self.scrobble.track.has_itunes_store_data:
      self.scrobble.load_itunes_store_data()
      self.emit_scrobble_ui_update_signals.emit(self.scrobble)