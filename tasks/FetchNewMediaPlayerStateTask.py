from PySide2 import QtCore

class FetchNewMediaPlayerStateTask(QtCore.QObject, QtCore.QRunnable):  
  finished = QtCore.Signal(dict)

  def __init__(self, history_reference):
    QtCore.QObject.__init__(self)
    QtCore.QRunnable.__init__(self)

    # Store a reference to the history view model
    self.history_reference = history_reference

    self.setAutoDelete(True)

  def run(self):
    '''Synchronously run code that makes external requests to the media player'''

    media_player_state = None

    if self.history_reference:
      media_player_state = self.history_reference.media_player.get_state()

    # Emit signal to call processing function in view model
    self.finished.emit(media_player_state)
