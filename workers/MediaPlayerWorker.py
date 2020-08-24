from PySide2 import QtCore

class MediaPlayerWorker(QtCore.QObject):  
  finished_getting_media_player_data = QtCore.Signal(dict)

  def __init__(self):
    QtCore.QObject.__init__(self)

    # Store a reference to the history view model
    self.history_reference = None

  @QtCore.Slot()
  def get_new_media_player_data(self): # Python-only slots don't need to be camel cased
    '''Synchronously run code that makes external requests to the media player'''

    media_player_state = None

    if self.history_reference:
      media_player_state = self.history_reference.media_player.get_state()

    # Emit signal to call processing function in view model
    self.finished_getting_media_player_data.emit(media_player_state)
