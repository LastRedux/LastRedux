from PySide2 import QtCore

from datatypes.Scrobble import Scrobble

class LoadAdditionalScrobbleDataTask(QtCore.QObject, QtCore.QRunnable):
  emit_scrobble_ui_update_signals = QtCore.Signal(Scrobble)
  finished = QtCore.Signal()

  def __init__(self, view_model, scrobble: Scrobble):
    QtCore.QObject.__init__(self)
    QtCore.QRunnable.__init__(self)

    self.__view_model = view_model
    self.scrobble = scrobble
    self.setAutoDelete(True)

  def run(self):
    '''Fetch and attach information from Last.fm and Spotify to the passed Scrobble object and emit signals to update that specific scrobble in the UI'''

    if not self.__view_model.get_is_enabled():
      return

    # Load Last.fm data
    self.scrobble.load_lastfm_data()

    if not self.__view_model.get_is_enabled():
      return

    self.emit_scrobble_ui_update_signals.emit(self.scrobble)
    
    # Load Spotify data
    self.scrobble.load_spotify_data()

    if not self.__view_model.get_is_enabled():
      return

    self.emit_scrobble_ui_update_signals.emit(self.scrobble)

    # Load iTunes images if needed
    if self.scrobble.album and not self.scrobble.album.image_url:
      self.scrobble.fetch_and_load_itunes_store_images()
      self.emit_scrobble_ui_update_signals.emit(self.scrobble)

    self.finished.emit()