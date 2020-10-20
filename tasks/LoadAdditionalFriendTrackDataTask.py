from PySide2 import QtCore

from datatypes.Track import Track

class LoadAdditionalFriendTrackDataTask(QtCore.QObject, QtCore.QRunnable):
  finished = QtCore.Signal(int)

  def __init__(self, track: Track, row_in_friends_list: int):
    QtCore.QObject.__init__(self)
    QtCore.QRunnable.__init__(self)
    self.track = track
    self.setAutoDelete(True)
    self.row_in_friends_list = row_in_friends_list

  def run(self):
    '''Fetch and attach information from Last.fm and iTunes to the passed Track object '''

    self.track.load_lastfm_data()
    self.track.load_spotify_data()
    self.finished.emit(self.row_in_friends_list)