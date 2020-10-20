from PySide2 import QtCore

from datatypes.Scrobble import Scrobble

class LoadAdditionalScrobbleDataTask(QtCore.QObject, QtCore.QRunnable):
  emit_scrobble_ui_update_signals = QtCore.Signal(Scrobble)
  finished = QtCore.Signal()

  def __init__(self, scrobble: Scrobble, should_load_spotify_data, is_part_of_initial_batch=False):
    QtCore.QObject.__init__(self)
    QtCore.QRunnable.__init__(self)

    self.scrobble = scrobble
    self.should_load_spotify_data = should_load_spotify_data
    self.is_part_of_initial_batch = is_part_of_initial_batch
    self.setAutoDelete(True)

  def run(self):
    '''Fetch and attach information from Last.fm and Spotify to the passed Scrobble object and emit signals to update that specific scrobble in the UI'''

    # Refresh details view with Last.fm details if it doesn't exist
    if not self.scrobble.has_lastfm_data:
      self.scrobble.load_lastfm_data()
      self.emit_scrobble_ui_update_signals.emit(self.scrobble)

    # Don't load Spotify data for tracks that are being loaded from Last.fm as recent tracks or tracks that already have Spotify data
    if not self.should_load_spotify_data or self.scrobble.has_spotify_data:
      if self.is_part_of_initial_batch:
        self.finished.emit()
      
      return

    # Get artist image and album art from Spotify
    self.scrobble.load_spotify_data()
    self.emit_scrobble_ui_update_signals.emit(self.scrobble)

    if self.is_part_of_initial_batch:
      self.finished.emit()