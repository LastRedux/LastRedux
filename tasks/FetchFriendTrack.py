from datatypes.FriendTrack import FriendTrack
from datetime import datetime

from PySide2 import QtCore
from loguru import logger

from util.LastfmApiWrapper import LastfmApiWrapper

class FetchFriendTrack(QtCore.QObject, QtCore.QRunnable):
  finished = QtCore.Signal(dict, int)

  def __init__(self, lastfm: LastfmApiWrapper, username: str, friend_index: int):
    QtCore.QObject.__init__(self)
    QtCore.QRunnable.__init__(self)
    self.lastfm = lastfm
    self.username = username
    self.friend_index = friend_index
    self.setAutoDelete(True)

  def run(self):
    '''Load the friend's most recent scrobble from Last.fm'''

    scrobble = self.lastfm.get_last_scrobble_by_username(self.username)

    self.finished.emit(scrobble, self.friend_index)