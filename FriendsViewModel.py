from datatypes.lastfm.LastfmUser import LastfmUser
from typing import List
from datetime import datetime

from PySide2 import QtCore

from ApplicationViewModel import ApplicationViewModel
from tasks.FetchFriendTrack import FetchFriendTrack
from tasks.FetchFriendsTask import FetchFriendsTask
from tasks.FetchFriendTrackImage import FetchFriendTrackImage
from datatypes.Track import Track
from datatypes.Friend import Friend

class FriendsViewModel(QtCore.QObject):
  # Qt Property signals
  is_enabled_changed = QtCore.Signal()
  should_show_loading_indicator_changed = QtCore.Signal()
  
  # Friends list model signals
  begin_refresh_friends = QtCore.Signal()
  end_refresh_friends = QtCore.Signal()
  is_loading_changed = QtCore.Signal()
  album_image_url_changed = QtCore.Signal(int)

  def __init__(self):
    QtCore.QObject.__init__(self)

    self.__application_reference: ApplicationViewModel = None
    self.__is_enabled: bool = False
    self.reset_state()

  def reset_state(self):
    self.friends: List[Friend] = []
    self.__friends_with_track_loaded_count: int = 0
    self.__should_show_loading_indicator: bool = False
    self.__is_loading: bool = False
    # self.__previous_friends = None

  # --- Slots ---

  @QtCore.Slot(bool)
  def loadFriends(self, was_app_refocused: bool=False):
    '''Initiate the process of loading (or reloading) the user's friends and their tracks'''

    if self.__is_enabled:
      # Enable loading indicator if there are no friends (initial page load) or the window was refocused
      if not self.friends or was_app_refocused:
        self.__should_show_loading_indicator = True
        self.should_show_loading_indicator_changed.emit()

      # Fetch friends if they aren't already being fetched
      if not self.__is_loading:
        self.__is_loading = True
        self.is_loading_changed.emit()

        fetch_friends_task = FetchFriendsTask(self.__application_reference.lastfm)
        fetch_friends_task.finished.connect(self.__handle_fetched_lastfm_friends)
        QtCore.QThreadPool.globalInstance().start(fetch_friends_task)

  # --- Private Methods ---

  def __handle_fetched_lastfm_friends(self, lastfm_users: List[LastfmUser]):
    '''Create Friend objects from Last.fm friends and run tasks to fetch their current/recent tracks'''

    if not self.__is_enabled:
      return
    
    # Create two sets of usernames to compare for differences (check if any friends were added/removed)
    new_usernames = [user.username for user in lastfm_users]
    current_usernames = [friend.username for friend in self.friends] # Will be [] on first load
    friends_changed = set(new_usernames) != set(current_usernames)

    # Load and sort new list of friends if it doesn't match the current one 
    if friends_changed:
      self.begin_refresh_friends.emit()
      
      # Build Friend objects and sort them alphabetically by username
      self.friends = sorted(
        [Friend.from_lastfm_user(user) for user in lastfm_users],
        key=lambda friend: friend.username.lower()
      )

      # Update UI with friends (just friend, no track)
      self.end_refresh_friends.emit()

    # Reset loading tracker
    self.__friends_with_track_loaded_count = 0

    # Load each friend's most recent/currently playing track
    for index, friend in enumerate(self.friends):
      load_friends_track_task = FetchFriendTrack(self.__application_reference.lastfm, friend, index)
      load_friends_track_task.finished.connect(self.__handle_friend_track_fetched)
      QtCore.QThreadPool.globalInstance().start(load_friends_track_task)

  def __handle_friend_track_fetched(self, friend_track, friend_index):
    if not self.__is_enabled:
      return

    friend = self.friends[friend_index]
    friend.track = friend_track # Could be None but that's okay
    friend.is_loading = False

    # Increment regardless of whether a track was actually found, we're keeping track of loading
    self.__friends_with_track_loaded_count += 1

    # Update UI when the last friend is loaded
    if self.__friends_with_track_loaded_count == len(self.friends):      
      # Move friends currently playing music to the top
      self.friends = sorted(self.friends, key=lambda friend: bool(friend.is_track_playing), reverse=True) # bool() because it might be None

      # Move friends with no track to the bottom
      self.friends = sorted(self.friends, key=lambda friend: bool(friend.track.title) if friend.track else False, reverse=True)

      # WIP CODE for comparing friends - not working
      # Only refresh friends if new friend activity is different
      # should_refresh_friends = True
      
      # consistencies = 0
      # if self.previous_friends:
      #   if len(self.previous_friends) == len(self.friends):
      #     for i in range(len(self.friends)):
      #       if self.friends[i].equals(self.previous_friends[i]):
      #         consistencies += 1
          
      #     print(consistencies)
      #     if consistencies == len(self.friends):
      #       should_refresh_friends = False
      # self.previous_friends = self.friends

      # if should_refresh_friends:
        # Refresh UI with friend tracks
      
      self.end_refresh_friends.emit()

      self.__is_loading = False
      self.is_loading_changed.emit()
      
      # Update loading indicator on tab bar if needed
      if self.__should_show_loading_indicator:
        self.__should_show_loading_indicator = False
        self.should_show_loading_indicator_changed.emit()

      # Start loading album art for friend tracks
      for row, friend in enumerate(self.friends):
        if not friend.is_track_playing:
          continue

        fetch_track_image_task = FetchFriendTrackImage(friend.track, row)
        fetch_track_image_task.finished.connect(lambda row_in_list: self.album_image_url_changed.emit(row_in_list))
        QtCore.QThreadPool.globalInstance().start(fetch_track_image_task)

  # --- Qt Property Getters and Setters ---

  def set_application_reference(self, new_reference):
    if not new_reference:
      return

    self.__application_reference = new_reference

    self.__application_reference.is_logged_in_changed.connect(lambda: self.set_is_enabled(self.__application_reference.is_logged_in))

  def set_is_enabled(self, is_enabled):
    self.__is_enabled = is_enabled
    self.is_enabled_changed.emit()

    if is_enabled:
      self.reset_state()
    else:
      self.begin_refresh_friends.emit()
      self.reset_state()
      self.should_show_loading_indicator_changed.emit()
      self.end_refresh_friends.emit()

    self.is_loading_changed.emit()
  
  # --- Qt Properties ---

  applicationReference = QtCore.Property(ApplicationViewModel, lambda self: self.__application_reference, set_application_reference)
  isEnabled = QtCore.Property(bool, lambda self: self.__is_enabled, set_is_enabled, notify=is_enabled_changed)
  shouldShowLoadingIndicator = QtCore.Property(bool, lambda self: self.__should_show_loading_indicator, notify=should_show_loading_indicator_changed)
  isLoading = QtCore.Property(bool, lambda self: self.__is_loading, notify=is_loading_changed)