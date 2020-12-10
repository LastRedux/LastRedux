from datetime import datetime

from PySide2 import QtCore
from loguru import logger

from util.LastfmApiWrapper import LastfmApiWrapper
from datatypes.Track import Track
from datatypes.Friend import Friend

class FetchFriendTrack(QtCore.QObject, QtCore.QRunnable):
  finished = QtCore.Signal(dict, int)

  def __init__(self, lastfm_instance: LastfmApiWrapper, friend: Friend, friend_index: int):
    QtCore.QObject.__init__(self)
    QtCore.QRunnable.__init__(self)
    self.lastfm_instance = lastfm_instance
    self.friend = friend
    self.friend_index = friend_index
    self.setAutoDelete(True)

  def run(self):
    '''Load the passed Friend's most recent scrobble from Last.fm'''

    # Fetch a friend's most recent scrobble (just one)
    last_scrobble_response = self.lastfm_instance.get_recent_scrobbles(self.friend.username, 1)

    last_scrobble = None

    try:
      last_scrobble = last_scrobble_response['recenttracks']['track'][0]
    except IndexError:
      # Don't do anything, we want to return None
      pass

    self.finished.emit(last_scrobble, self.friend_index)