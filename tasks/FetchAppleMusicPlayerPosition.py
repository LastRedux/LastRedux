from PySide2 import QtCore

class FetchAppleMusicPlayerPosition(QtCore.QObject, QtCore.QRunnable):  
  finished = QtCore.Signal(dict)

  def __init__(self, media_player):
    QtCore.QObject.__init__(self)
    QtCore.QRunnable.__init__(self)
    self.media_player = media_player
    self.setAutoDelete(True)

  def run(self):
    '''Fetch current playback position timestamp using Apple Music AppleScript commands'''

    player_position = self.media_player.get_player_position()
    self.finished.emit(player_position)