from PySide2 import QtCore

class FetchNewMediaPlayerStateTask(QtCore.QObject, QtCore.QRunnable):  
  finished = QtCore.Signal(dict)

  def __init__(self, media_player):
    QtCore.QObject.__init__(self)
    QtCore.QRunnable.__init__(self)
    self.media_player = media_player
    self.setAutoDelete(True)

  def run(self):
    '''Synchronously run code that makes external requests to the media player'''

    media_player_state = None

    if self.media_player:
      media_player_state = self.media_player.get_state()

    # Emit signal to call processing function in view model
    self.finished.emit(media_player_state)
