from PySide2 import QtCore

from models.Scrobble import Scrobble

class ApiRequestWorker(QtCore.QObject):  
  call_set_additional_scrobble_data = QtCore.Signal(Scrobble)
  emit_scrobble_ui_update_signals = QtCore.Signal(Scrobble)
  finished = QtCore.Signal(Scrobble)

  def __init__(self):
    QtCore.QObject.__init__(self)

  @QtCore.Slot()
  def set_additional_scrobble_data(self, scrobble):
    '''Fetch and attach information from Last.fm to the __current_scrobble Scrobble object and emit signals to update that specific scrobble in the UI'''

    # Refresh details view with Last.fm details
    scrobble.load_lastfm_data()
    self.emit_scrobble_ui_update_signals.emit(scrobble)
    
    # Get artist image and album art from iTunes
    # TODO: Only update artist/album image URL instead of entire scrobble data
    scrobble.load_itunes_store_data()
    self.emit_scrobble_ui_update_signals.emit(scrobble)

    # # Refresh details view with similar artist images from iTunes
    # scrobble.load_similar_artist_images()
    # self.emit_scrobble_ui_update_signals.emit(scrobble)

    # Pass self as parameter to let the view model kill the thread worker's thread
    self.finished.emit(scrobble)