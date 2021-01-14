from util.lastfm.LastfmUser import LastfmUser
from PySide2 import QtCore

from util.lastfm import LastfmApiWrapper

class FetchFriends(QtCore.QObject, QtCore.QRunnable):
  finished = QtCore.Signal(list)

  def __init__(self, lastfm: LastfmApiWrapper):
    QtCore.QObject.__init__(self)
    QtCore.QRunnable.__init__(self)
    self.lastfm = lastfm
    self.setAutoDelete(True)

  def run(self) -> None:
    friends = self.lastfm.get_friends()
    self.finished.emit(friends)