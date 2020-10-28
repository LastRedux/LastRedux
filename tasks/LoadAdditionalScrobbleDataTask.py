from PySide2 import QtCore

from datatypes.Scrobble import Scrobble

class LoadAdditionalScrobbleDataTask(QtCore.QObject, QtCore.QRunnable):
  emit_scrobble_ui_update_signals = QtCore.Signal(Scrobble)
  finished = QtCore.Signal()

  def __init__(self, scrobble: Scrobble):
    QtCore.QObject.__init__(self)
    QtCore.QRunnable.__init__(self)

    self.scrobble = scrobble
    self.setAutoDelete(True)

  def run(self):
    '''Fetch and attach information from Last.fm and Spotify to the passed Scrobble object and emit signals to update that specific scrobble in the UI'''

    # Load Last.fm data
    self.scrobble.load_lastfm_data()
    self.emit_scrobble_ui_update_signals.emit(self.scrobble)
    
    # Load Spotify data
    self.scrobble.load_spotify_data()
    self.emit_scrobble_ui_update_signals.emit(self.scrobble)

    # Load iTunes images if needed
    if not self.scrobble.album.image_url:
      self.scrobble.fetch_and_load_itunes_store_images()
      self.emit_scrobble_ui_update_signals.emit(self.scrobble)

    self.finished.emit()