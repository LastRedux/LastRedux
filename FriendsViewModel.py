import logging
from typing import List

from PySide2 import QtCore

from ApplicationViewModel import ApplicationViewModel
from tasks import FetchFriends, FetchFriendScrobble, FetchFriendScrobbleArt
from util.lastfm import LastfmUser
from datatypes.Friend import Friend
from datatypes.FriendScrobble import FriendScrobble

class FriendsViewModel(QtCore.QObject):
  # Qt Property signals
  is_enabled_changed = QtCore.Signal()
  should_show_loading_indicator_changed = QtCore.Signal()
  
  # Friends list model signals
  begin_refresh_friends = QtCore.Signal()
  end_refresh_friends = QtCore.Signal()
  is_loading_changed = QtCore.Signal()
  album_image_url_changed = QtCore.Signal(int)

  def __init__(self) -> None:
    QtCore.QObject.__init__(self)

    self.__application_reference: ApplicationViewModel = None
    self.__is_enabled: bool = False
    self.reset_state()

  def reset_state(self) -> None:
    self.friends: List[Friend] = []
    self.__did_a_friend_track_change: bool = None
    self.__new_friends_with_track_loaded_count: int = 0
    self.__should_show_loading_indicator: bool = False
    self.__is_loading: bool = False

  # --- Slots ---

  @QtCore.Slot(bool)
  def loadFriends(self, was_app_refocused: bool=False) -> None:
    '''Initiate the process of loading (or reloading) the user's friends and their tracks'''

    if not self.__is_enabled:
      return

    if self.__application_reference.is_offline:
      # Skip request if offline
      logging.debug('Offline, not loading profile')
      return

    # Don't refetch friends if they're already loading
    if self.__is_loading:
      return
    
    # Enable loading indicator if there are no friends (initial page load) or the window was refocused
    # if not self.friends or was_app_refocused:

    # Update loading indicator
    self.__should_show_loading_indicator = True
    self.should_show_loading_indicator_changed.emit()
    self.__is_loading = True
    self.is_loading_changed.emit()

    # Fetch and load friends
    fetch_friends_task = FetchFriends(lastfm=self.__application_reference.lastfm)
    fetch_friends_task.finished.connect(self.__handle_lastfm_friends_fetched)
    QtCore.QThreadPool.globalInstance().start(fetch_friends_task)

  # --- Private Methods ---

  def __handle_lastfm_friends_fetched(self, lastfm_users: List[LastfmUser]) -> None:
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
    self.__new_friends_with_track_loaded_count = 0
    self.__did_a_friend_track_change = False

    # Load each friend's most recent/currently playing track
    for i, friend in enumerate(self.friends):
      load_friend_scrobble_task = FetchFriendScrobble(
        lastfm=self.__application_reference.lastfm, 
        username=friend.username, 
        friend_index=i
      )
      load_friend_scrobble_task.finished.connect(self.__handle_friend_scrobble_fetched)
      QtCore.QThreadPool.globalInstance().start(load_friend_scrobble_task)

  def __handle_friend_scrobble_fetched(self, new_friend_scrobble: FriendScrobble, friend_index: int) -> None:
    if not self.__is_enabled:
      return

    friend = self.friends[friend_index]
    friend.is_loading = False

    if (
      # There wasn't a scrobble but now there is one
      not friend.last_scrobble and new_friend_scrobble

      # Latest scrobble changed
      or friend.last_scrobble != new_friend_scrobble
    ):
      friend.last_scrobble = new_friend_scrobble
      self.__did_a_friend_track_change = True
      
    # Increment regardless of whether a track was actually found, we're keeping track of loading
    self.__new_friends_with_track_loaded_count += 1

    # Update UI when the last friend is loaded
    if self.__new_friends_with_track_loaded_count == len(self.friends):      
      # Move friends currently playing music to the top
      self.friends = sorted(
        self.friends,
        key=lambda friend: bool(friend.last_scrobble.is_playing) if friend.last_scrobble else False, # bool because it might be None
        reverse=True
      )

      # Move friends with no track to the bottom
      self.friends = sorted(
        self.friends, 
        key=lambda friend: bool(friend.last_scrobble),
        reverse=True
      )

      if not self.friends or self.__did_a_friend_track_change:
        self.begin_refresh_friends.emit()
        self.end_refresh_friends.emit()

        # Start loading album art for friend tracks
        for row, friend in enumerate(self.friends):
          if not friend.last_scrobble or not friend.last_scrobble.is_playing:
            continue

          fetch_album_art_task = FetchFriendScrobbleArt(
            art_provider=self.applicationReference.art_provider,
            friend_scrobble=friend.last_scrobble,
            row_in_friends_list=row
          )
          fetch_album_art_task.finished.connect(
            lambda row_in_list: self.album_image_url_changed.emit(row_in_list)
          )
          QtCore.QThreadPool.globalInstance().start(fetch_album_art_task)

      self.__is_loading = False
      self.is_loading_changed.emit()
      
      # Update loading indicator on tab bar if needed
      if self.__should_show_loading_indicator:
        self.__should_show_loading_indicator = False
        self.should_show_loading_indicator_changed.emit()

  # --- Qt Property Getters and Setters ---

  def set_application_reference(self, new_reference: ApplicationViewModel) -> None:
    if not new_reference:
      return

    self.__application_reference = new_reference

    self.__application_reference.is_logged_in_changed.connect(
      lambda: self.set_is_enabled(self.__application_reference.is_logged_in)
    )

  def set_is_enabled(self, is_enabled: bool) -> None:
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

  applicationReference = QtCore.Property(
    type=ApplicationViewModel,
    fget=lambda self: self.__application_reference, 
    fset=set_application_reference
  )

  isEnabled = QtCore.Property(
    type=bool, 
    fget=lambda self: self.__is_enabled, 
    fset=set_is_enabled, 
    notify=is_enabled_changed
  )

  shouldShowLoadingIndicator = QtCore.Property(
    type=bool,
    fget=lambda self: self.__should_show_loading_indicator, 
    notify=should_show_loading_indicator_changed
  )

  isLoading = QtCore.Property(
    type=bool, 
    fget=lambda self: self.__is_loading, 
    notify=is_loading_changed
  )