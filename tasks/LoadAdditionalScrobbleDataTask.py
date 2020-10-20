from PySide2 import QtCore

from datatypes.Scrobble import Scrobble

class LoadAdditionalScrobbleDataTask(QtCore.QObject, QtCore.QRunnable):
  emit_scrobble_ui_update_signals = QtCore.Signal(Scrobble)

  def __init__(self, scrobble: Scrobble):
    QtCore.QObject.__init__(self)
    QtCore.QRunnable.__init__(self)

    self.scrobble = scrobble
    self.setAutoDelete(True)

  def run(self):
    '''Fetch and attach information from Last.fm and Spotify to the passed Scrobble object and emit signals to update that specific scrobble in the UI'''

    # Refresh details view with Last.fm details if it doesn't exist
    if not self.scrobble.has_lastfm_data:
      self.scrobble.load_lastfm_data()
      self.emit_scrobble_ui_update_signals.emit(self.scrobble)

    # Get artist image and album art from Spotify
    self.scrobble.load_spotify_data()
    self.emit_scrobble_ui_update_signals.emit(self.scrobble)