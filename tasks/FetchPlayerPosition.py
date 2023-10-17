from PySide6 import QtCore

from plugins.MediaPlayerPlugin import MediaPlayerPlugin

class FetchPlayerPosition(QtCore.QObject, QtCore.QRunnable):  
  finished = QtCore.Signal(float)

  def __init__(self, media_player: MediaPlayerPlugin):
    QtCore.QObject.__init__(self)
    QtCore.QRunnable.__init__(self)
    self.media_player = media_player
    self.setAutoDelete(True)

  def run(self):
    player_position = self.media_player.get_player_position()
    self.finished.emit(player_position)