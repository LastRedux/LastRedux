from datatypes.Track import Track
from datetime import datetime

from datatypes.Friend import Friend
from PySide2 import QtCore

from tasks.FetchFriendTrack import FetchFriendTrack
from tasks.FetchFriendsTask import FetchFriendsTask
from tasks.FetchFriendTrackImage import FetchFriendTrackImage
import util.LastfmApiWrapper as lastfm

class FriendsViewModel(QtCore.QObject):
  begin_refresh_friends = QtCore.Signal()
  end_refresh_friends = QtCore.Signal()
  should_show_loading_indicator_changed = QtCore.Signal()
  album_image_url_changed = QtCore.Signal(int)

  def __init__(self):
    QtCore.QObject.__init__(self)

    self.__should_show_loading_indicator = False
    self.lastfm_instance = lastfm.get_static_instance()
    self.friends = []
    self.__friends_with_track_loaded_count = 0
    self.__is_loading = False

  # --- Slots ---

  @QtCore.Slot()
  @QtCore.Slot(bool)
  def loadFriends(self, force_loading_indicator=False):
    '''Initiate the process of loading (or reloading) the user's friends and their tracks'''

    # Enable loading indicator if initial load or window reactivated
    if not self.friends or force_loading_indicator:
      self.__should_show_loading_indicator = True
      self.should_show_loading_indicator_changed.emit()

    # Fetch friends if they aren't already being fetched
    if not self.__is_loading:
      self.__is_loading = True

      fetch_friends_task = FetchFriendsTask(self.lastfm_instance)
      fetch_friends_task.finished.connect(self.__handle_fetched_lastfm_friends)
      QtCore.QThreadPool.globalInstance().start(fetch_friends_task)

  # --- Private Methods ---
  
  def __handle_fetched_lastfm_friends(self, new_lastfm_friends):
    '''Create Friend objects from Last.fm friends and run tasks to fetch their current/recent tracks'''

    # Create two sets of usernames to compare for differences (check if any friends were added/removed)
    new_usernames = [lastfm_friend['name'] for lastfm_friend in new_lastfm_friends]
    current_usernames = [friend.username for friend in self.friends] # Will be [] on first load
    friends_changed = set(new_usernames) != set(current_usernames)

    # Load and sort new list of friends if it doesn't match the current one 
    if friends_changed:
      self.begin_refresh_friends.emit()
      
      # Build Friend objects and sort them alphabetically by username
      self.friends = sorted(
        [Friend.build_from_lastfm_friend(lastfm_friend) for lastfm_friend in new_lastfm_friends],
        key=lambda friend: friend.username.lower()
      )

      # Update UI with friends (just friend, no track)
      self.end_refresh_friends.emit()

    # Reset loading tracker
    self.__friends_with_track_loaded_count = 0

    # Load each friend's most recent/currently playing track
    for index, friend in enumerate(self.friends):
      load_friends_track_task = FetchFriendTrack(self.lastfm_instance, friend, index)
      load_friends_track_task.finished.connect(self.__handle_friend_track_fetched)
      QtCore.QThreadPool.globalInstance().start(load_friends_track_task)

  def __handle_friend_track_fetched(self, lastfm_track, friend_index):
    friend = self.friends[friend_index]
    should_load_track = False

    if lastfm_track:
      friend.is_track_playing = lastfm_track.get('@attr', {}).get('nowplaying') == 'true'

      # Check if scrobble was recent enough if it isn't playing
      if friend.is_track_playing:
        should_load_track = True
      else:
        scrobble_time = datetime.fromtimestamp(int(lastfm_track['date']['uts']))
        delta = datetime.now() - scrobble_time

        # Only load scrobble if it's within the last 24 hours (86400 seconds)
        if delta.total_seconds() <= 86400:
          should_load_track = True

    if should_load_track:
      friend.track = Track.build_from_lastfm_recent_track(lastfm_track)
    
    friend.is_loading = False

    # Increment regardless of whether a track was actually found, we're keeping track of loading
    self.__friends_with_track_loaded_count += 1

    # Update UI when the last friend is loaded
    if self.__friends_with_track_loaded_count == len(self.friends):      
      # Move friends currently playing music to the top
      self.friends = sorted(self.friends, key=lambda friend: bool(friend.is_track_playing), reverse=True) # bool() because it might be None

      # Move friends with no track to the bottom
      self.friends = sorted(self.friends, key=lambda friend: bool(friend.track.title) if friend.track else False, reverse=True)

      # Refresh UI with friend tracks
      self.end_refresh_friends.emit()
      self.__is_loading = False
      
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
  
  # --- Qt Properties ---

  shouldShowLoadingIndicator = QtCore.Property(bool, lambda self: self.__should_show_loading_indicator, notify=should_show_loading_indicator_changed)