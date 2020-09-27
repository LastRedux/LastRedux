from PySide2 import QtCore

from tasks.FetchFriendsTask import FetchFriendsTask
import util.LastfmApiWrapper as lastfm

class FriendsViewModel(QtCore.QObject):
  begin_refresh_friends = QtCore.Signal()
  end_refresh_friends = QtCore.Signal()
  friend_changed = QtCore.Signal()

  def __init__(self):
    QtCore.QObject.__init__(self)

    self.lastfm_instance = lastfm.get_static_instance()
    self.friends = []

  def get_friends(self):
    return self.friends

  # --- Slots ---

  @QtCore.Slot()
  def loadFriends(self):
    def __load_friends(new_friends):
      # old_friend_count = len(self.friends)
  
      # if len(new_friends) != old_friend_count:
          # A new friend was added since the last check
      self.begin_refresh_friends.emit()
      self.friends = new_friends
      self.end_refresh_friends.emit()
      # self.end_refresh_friends.emit()
      # else:
      #     # Same number of friends but songs may have changed
      #     for friend in new_friends:
      #         print()
      #         # if friend['']

    fetch_friends_task = FetchFriendsTask(self.lastfm_instance)
    fetch_friends_task.finished.connect(__load_friends)
    QtCore.QThreadPool.globalInstance().start(fetch_friends_task)