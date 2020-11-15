from loguru import logger
from PySide2 import QtCore

from tasks.LoadFriendsTracks import LoadFriendsTracks
from tasks.FetchFriendsTask import FetchFriendsTask
from tasks.FetchFriendTrackImage import FetchFriendTrackImage
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

  # --- Qt Property Getters and Setters ---

  def get_friends(self):
    return self.friends

  # --- Private Methods ---

  def __load_friends(self, lastfm_friends):
    logger.trace(f'Fetched Last.fm friend data for friends view')

    # Load list of friends (without tracks)
    self.begin_refresh_friends.emit()
    self.friends = lastfm_friends.copy()
    self.end_refresh_friends.emit()

    # Load each friend's most recent/currently playing track
    self.begin_refresh_friends.emit()
    load_friends_tracks_task = LoadFriendsTracks(self.lastfm_instance, self.friends)
    load_friends_tracks_task.finished.connect(self.__handle_fetch_friends_tracks_finished)
    QtCore.QThreadPool.globalInstance().start(load_friends_tracks_task)

  def __handle_fetch_friends_tracks_finished(self):
    ''''''

    # Move friends currently playing music to the top
    self.friends = sorted(self.friends, key=lambda friend: friend.is_track_playing, reverse=True)

    # Move friends with no track to the bottom
    self.friends = sorted(self.friends, key=lambda friend: bool(friend.track.title) if friend.track else False, reverse=True)

    self.end_refresh_friends.emit()
    self.__is_loading = False
    
    # Update loading indicator on tab bar if needed
    if self.__should_show_loading_indicator:
      self.__should_show_loading_indicator = False
      self.should_show_loading_indicator_changed.emit()

    for row, friend in enumerate(self.friends):
      if not friend.is_track_playing:
        continue

      fetch_track_image_task = FetchFriendTrackImage(friend.track, row)
      fetch_track_image_task.finished.connect(lambda row_in_list: self.album_image_url_changed.emit(row_in_list))
      QtCore.QThreadPool.globalInstance().start(fetch_track_image_task)
  
  # --- Slots ---

  @QtCore.Slot()
  @QtCore.Slot(bool)
  def loadFriends(self, force_loading_indicator=False):
    # Enable loading indicator if initial load or window reactivated
    if not self.friends or force_loading_indicator:
      self.__should_show_loading_indicator = True
      self.should_show_loading_indicator_changed.emit()

    # Fetch friends if they aren't already being fetched
    if not self.__is_loading:
      self.__is_loading = True

      fetch_friends_task = FetchFriendsTask(self.lastfm_instance)
      fetch_friends_task.finished.connect(self.__load_friends)
      QtCore.QThreadPool.globalInstance().start(fetch_friends_task)
  
  shouldShowLoadingIndicator = QtCore.Property(bool, lambda self: self.__should_show_loading_indicator, notify=should_show_loading_indicator_changed)