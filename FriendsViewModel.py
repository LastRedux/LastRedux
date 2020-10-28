from loguru import logger
from PySide2 import QtCore

from tasks.FetchFriendsTask import FetchFriendsTask
from tasks.LoadAdditionalFriendTrackDataTask import LoadAdditionalFriendTrackDataTask
import util.LastfmApiWrapper as lastfm

class FriendsViewModel(QtCore.QObject):
  begin_refresh_friends = QtCore.Signal()
  end_refresh_friends = QtCore.Signal()
  friend_changed = QtCore.Signal()
  should_show_loading_indicator_changed = QtCore.Signal()
  album_image_url_changed = QtCore.Signal(int)

  def __init__(self):
    QtCore.QObject.__init__(self)

    self.__should_show_loading_indicator = False
    self.lastfm_instance = lastfm.get_static_instance()
    self.friends = []
    self.__is_loading = False

  def get_friends(self):
    return self.friends

  # --- Slots ---

  @QtCore.Slot()
  @QtCore.Slot(bool)
  def loadFriends(self, force_loading_indicator=False):
    def __load_friends(new_friends):
      logger.trace(f'Fetched Last.fm friend data for friends view')
      self.begin_refresh_friends.emit()
      self.friends = new_friends.copy()
      self.end_refresh_friends.emit()

      for row, friend in enumerate(self.friends):
        if friend.is_track_playing:
          load_additional_friend_track_data = LoadAdditionalFriendTrackDataTask(friend.track, row)
          load_additional_friend_track_data.finished.connect(lambda row_in_friends_list: self.album_image_url_changed.emit(row_in_friends_list))
          QtCore.QThreadPool.globalInstance().start(load_additional_friend_track_data)
      
      # Update loading indicator on tab bar if needed
      if self.__should_show_loading_indicator:
        self.__should_show_loading_indicator = False
        self.should_show_loading_indicator_changed.emit()

      self.__is_loading = False

    # Enable loading indicator if initial load or window reactivated
    if not self.friends or force_loading_indicator:
      self.__should_show_loading_indicator = True
      self.should_show_loading_indicator_changed.emit()

    # Fetch friends if they aren't already being fetched
    if not self.__is_loading:
      self.__is_loading = True

      fetch_friends_task = FetchFriendsTask(self.lastfm_instance)
      fetch_friends_task.finished.connect(__load_friends)
      QtCore.QThreadPool.globalInstance().start(fetch_friends_task)
  
  shouldShowLoadingIndicator = QtCore.Property(bool, lambda self: self.__should_show_loading_indicator, notify=should_show_loading_indicator_changed)