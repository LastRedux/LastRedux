from PySide2 import QtCore

class FetchAppleMusicTrackCrop(QtCore.QObject, QtCore.QRunnable):  
  finished = QtCore.Signal(dict)

  def __init__(self, media_player):
    QtCore.QObject.__init__(self)
    QtCore.QRunnable.__init__(self)
    self.media_player = media_player
    self.setAutoDelete(True)

  def run(self):
    '''Fetch current track start and end timestamps using Apple Music AppleScript commands'''

    media_player_state = self.media_player.get_library_track_crop()
    self.finished.emit(media_player_state)