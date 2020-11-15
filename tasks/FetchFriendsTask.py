from PySide2 import QtCore

from datatypes.Friend import Friend

class FetchFriendsTask(QtCore.QObject, QtCore.QRunnable):
  finished = QtCore.Signal(list)

  def __init__(self, lastfm_instance):
    QtCore.QObject.__init__(self)
    QtCore.QRunnable.__init__(self)
    self.lastfm_instance = lastfm_instance
    self.setAutoDelete(True)

  def run(self):
    '''Fetch the user's Last.fm friends'''
    
    friends_response = self.lastfm_instance.get_friends()
    lastfm_friends = friends_response['friends']['user']

    # Build Friend objects
    friends = map(Friend.build_from_lastfm_friend, lastfm_friends)

    # Sort friends alphabetically by username
    friends = sorted(friends, key=lambda friend: friend.username.lower())
    
    self.finished.emit(friends)