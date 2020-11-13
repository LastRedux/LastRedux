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
    '''Return a list of the user's Last.fm friends and what they are/were listening to'''

    def lastfm_friend_to_friend(lastfm_friend):
      recent_track_response = self.lastfm_instance.get_recent_scrobbles(username=lastfm_friend['name'], count=1)

      recent_tracks = recent_track_response['recenttracks']['track']
      track = recent_tracks[0] if recent_tracks else None

      return Friend.build_from_lastfm_friend_and_recent_track(lastfm_friend, track)

    friends = list(map(lastfm_friend_to_friend, self.lastfm_instance.get_friends()['friends']['user']))
    
    self.finished.emit(friends)