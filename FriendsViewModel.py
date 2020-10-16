from PySide2 import QtCore

from tasks.FetchFriendsTask import FetchFriendsTask
from tasks.LoadAdditionalFriendTrackDataTask import LoadAdditionalFriendTrackDataTask
import util.LastfmApiWrapper as lastfm

class FriendsViewModel(QtCore.QObject):
  begin_refresh_friends = QtCore.Signal()
  end_refresh_friends = QtCore.Signal()
  friend_changed = QtCore.Signal()
  is_loading_changed = QtCore.Signal()
  album_image_url_changed = QtCore.Signal(int)

  def __init__(self):
    QtCore.QObject.__init__(self)

    self.__is_loading = False
    self.lastfm_instance = lastfm.get_static_instance()
    self.friends = []

  def get_friends(self):
    return self.friends

  # --- Slots ---

  @QtCore.Slot()
  def loadFriends(self):
    def __load_friends(new_friends):
      self.begin_refresh_friends.emit()
      self.friends = new_friends.copy()
      self.end_refresh_friends.emit()

      for row, friend in enumerate(self.friends):
        load_additional_friend_track_data = LoadAdditionalFriendTrackDataTask(friend.track, row)
        load_additional_friend_track_data.finished.connect(lambda row_in_friends_list: self.album_image_url_changed.emit(row_in_friends_list))
        QtCore.QThreadPool.globalInstance().start(load_additional_friend_track_data)
      
      # Update loading indicator on tab bar
      self.__is_loading = False
      self.is_loading_changed.emit()

    # Update loading indicator on tab bar
    self.__is_loading = True
    self.is_loading_changed.emit()

    # Fetch friends
    fetch_friends_task = FetchFriendsTask(self.lastfm_instance)
    fetch_friends_task.finished.connect(__load_friends)
    QtCore.QThreadPool.globalInstance().start(fetch_friends_task)
  
  isLoading = QtCore.Property(bool, lambda self: self.__is_loading, notify=is_loading_changed)