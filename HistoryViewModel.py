from dataclasses import asdict
from datatypes.TrackCrop import TrackCrop
from datatypes.MediaPlayerState import MediaPlayerState
import os
from datetime import datetime, timedelta
from typing import List
from util.lastfm import LastfmList
from util.lastfm.LastfmScrobble import LastfmScrobble
from plugins.MediaPlayerPlugin import MediaPlayerPlugin

from loguru import logger
from PySide2 import QtCore
from ScriptingBridge import SBApplication
from pypresence import Presence

from tasks import FetchPlayerPosition, LoadExternalScrobbleData, UpdateTrackLoveOnLastfm, FetchRecentScrobbles, SubmitScrobble, UpdateNowPlaying
from plugins.MockPlayerPlugin import MockPlayerPlugin
from plugins.macOS.music_app import MusicAppPlugin
from plugins.macOS.SpotifyPlugin import SpotifyPlugin
from ApplicationViewModel import ApplicationViewModel
from datatypes.Scrobble import Scrobble
import util.helpers as helpers

class HistoryViewModel(QtCore.QObject):
  # Constants
  __INITIAL_SCROBBLE_HISTORY_COUNT = int(os.environ.get('INITIAL_HISTORY_ITEMS', 30)) # 30 is the default but can be configured
  __CURRENT_SCROBBLE_INDEX = -1
  __NO_SELECTION_INDEX = -2

  # Qt Property changed signals
  is_enabled_changed = QtCore.Signal()
  current_scrobble_data_changed = QtCore.Signal()
  scrobble_percentage_changed = QtCore.Signal()
  is_player_paused_changed = QtCore.Signal()
  is_spotify_plugin_available_changed = QtCore.Signal()
  is_using_mock_player_changed = QtCore.Signal()
  selected_scrobble_changed = QtCore.Signal()
  selected_scrobble_index_changed = QtCore.Signal()
  should_show_loading_indicator_changed = QtCore.Signal()
  media_player_name_changed = QtCore.Signal()
  
  # Scrobble history list model signals
  pre_append_scrobble = QtCore.Signal()
  post_append_scrobble = QtCore.Signal()
  scrobble_album_image_changed = QtCore.Signal(int)
  scrobble_lastfm_is_loved_changed = QtCore.Signal(int)
  begin_refresh_history = QtCore.Signal()
  end_refresh_history = QtCore.Signal()

  # Signals handled from QML
  showNotification = QtCore.Signal(str, str)
  preloadProfileAndFriends = QtCore.Signal()

  def __init__(self) -> None:
    QtCore.QObject.__init__(self)

    # TODO: Figure out which things should be in reset_state

    self.__application_reference: ApplicationViewModel = None
    self.__is_enabled: bool = False
    
    # Initialize media player plugins
    self.__spotify_plugin = SpotifyPlugin()
    self.__music_app_plugin = MusicAppPlugin()
    self.__media_player: MediaPlayerPlugin = None
    self.__is_spotify_plugin_available = False # This is set to true if Spotify is installed
    
    # Set up Discord presence
    self.__is_discord_rpc_enabled = bool(os.environ.get('DISCORD_PRESENCE'))
    self.__discord_rpc = Presence('799678908819439646')

    if self.__is_discord_rpc_enabled and  helpers.is_discord_open():
      self.__discord_rpc.connect()

    logger.info(f'Discord RPC is set to {self.__is_discord_rpc_enabled}')

    # Settings
    # TODO: Move these properties to an App view model
    self.__is_submission_enabled: bool = None
    self.is_player_paused = False
    
    if os.environ.get('MOCK'):
      self.__media_player = MockPlayerPlugin()
    else:
      use_spotify = False
      spotify_app = SBApplication.applicationWithBundleIdentifier_('com.spotify.client')
      
      # TODO: Use better method to figure out if Spotify is installed without logged error
      if spotify_app:
        self.__is_spotify_plugin_available = True

        if spotify_app.isRunning():
          use_spotify = True
      
      if use_spotify:
        self.switchToMediaPlugin('spotify')
      else:
        # Use Music app plugin in all other cases since every Mac has it
        self.switchToMediaPlugin('musicApp')

    self.__media_player.stopped.connect(self.__handle_media_player_stopped)
    self.__media_player.playing.connect(self.__handle_media_player_playing)
    self.__media_player.paused.connect(self.__handle_media_player_paused)
    self.__media_player.cannot_scrobble_error.connect(
      lambda message: self.showNotification.emit('The track you\'re playing cannot be scrobbled', message)
    )
    self.media_player_name_changed.emit()

    # Start polling interval to check for new media player position
    self.__timer = QtCore.QTimer(self)
    self.__timer.timeout.connect(self.__fetch_new_media_player_position)

    self.reset_state()
  
  def reset_state(self) -> None:
    # Store Scrobble objects that have been submitted
    self.scrobble_history: List[Scrobble] = []

    # Keep track of whether the history view is loading data
    self.__should_show_loading_indicator = False

    # Keep track of how many scrobbles have their additional data loaded from Last.fm and Spotify
    self.__scrobbles_with_external_data_count = 0

    # Hold a Scrobble object for currently playing track (will later be submitted)
    self.__current_scrobble: Scrobble = None
    
    # Hold the index of the selected scrobble in the sidebar
    self.__selected_scrobble_index: int = None
    
    # Hold the Scrobble object at the __selected_scrobble_index
    # This can either be a copy of the current scrobble or one in the history
    self.selected_scrobble: Scrobble = None

    # Keep track of whether the current scrobble has hit the threshold for submission
    self.__current_scrobble_percentage: float = None
    self.__should_submit_current_scrobble = False
  
    # Keep track of furthest position reached in a song
    self.__furthest_player_position_reached: float = None

    # Keep track of how many poll ticks have passed since the playback position changed
    self.__cached_playback_position: float = None
    self.__ticks_since_position_change: int = None

    # Store the current track's crop values since they aren't part of the scrobble object
    self.__current_track_crop: TrackCrop = None

  # --- Qt Property Getters and Setters ---

  def set_application_reference(self, new_reference: ApplicationViewModel) -> None:
    if not new_reference:
      return
    
    self.__application_reference = new_reference
    self.__application_reference.is_logged_in_changed.connect(
      lambda: self.set_is_enabled(self.__application_reference.is_logged_in)
    )
    
  def get_selected_scrobble_index(self):
    '''Make the private selected scrobble index variable available to the UI'''
    
    if self.__selected_scrobble_index is None:
      # HistoryViewModel.__NO_SELECTION_INDEX represents no selection because Qt doesn't understand Python's None value
      return HistoryViewModel.__NO_SELECTION_INDEX

    return self.__selected_scrobble_index
  
  def set_selected_scrobble_index(self, new_index: int) -> None:
    if not self.__is_enabled:
      return
    
    # Prevent setting an illegal index with keyboard shortcuts
    if (
      # Prevent navigating before current scrobble
      new_index < HistoryViewModel.__CURRENT_SCROBBLE_INDEX

      or (
        # Prevent navigating to current scrobble when there isn't one
        new_index == HistoryViewModel.__CURRENT_SCROBBLE_INDEX
        and self.__current_scrobble is None
      )

      # Prevent navigating past scrobble history
      or new_index == len(self.scrobble_history)
    ):
      return
    
    self.__selected_scrobble_index = new_index
    self.selected_scrobble_index_changed.emit()

    if new_index == HistoryViewModel.__CURRENT_SCROBBLE_INDEX:
      self.selected_scrobble = self.__current_scrobble
    else:
      self.selected_scrobble = self.scrobble_history[new_index]
    
    # Update details view
    self.selected_scrobble_changed.emit()

  def set_is_enabled(self, is_enabled: bool) -> None:
    self.__is_enabled = is_enabled
    self.is_enabled_changed.emit()

    if is_enabled:
      # Reset view model
      self.reset_state()
      self.__media_player.request_initial_state()
      self.reloadHistory()
      self.preloadProfileAndFriends.emit()
      polling_interval = 100 if os.environ.get('MOCK') else 1000
      self.__timer.start(polling_interval)
    else:
      self.begin_refresh_history.emit()
      self.reset_state()
      self.end_refresh_history.emit()
      self.selected_scrobble_index_changed.emit()
      self.selected_scrobble_changed.emit() # This causes details pane to stop showing a scrobble
      self.current_scrobble_data_changed.emit()
      self.__timer.stop()

    self.should_show_loading_indicator_changed.emit()

  # --- Slots ---

  @QtCore.Slot()
  def reloadHistory(self):
    '''Reload recent scrobbles from Last.fm'''

    if (
      self.__INITIAL_SCROBBLE_HISTORY_COUNT == 0
      
      # Prevent reloading during onboarding
      or not self.__is_enabled

      # Prevent reloading while the view is already loading
      or self.__should_show_loading_indicator
    ):
      return

    # Update loading indicator
    self.__should_show_loading_indicator = True
    self.should_show_loading_indicator_changed.emit()

    # Reset scrobble history list
    self.begin_refresh_history.emit()
    self.scrobble_history = []
    self.end_refresh_history.emit()
    self.__scrobbles_with_external_data_count = 0

    # Fetch and load recent scrobbles
    fetch_recent_scrobbles_task = FetchRecentScrobbles(
      lastfm=self.__application_reference.lastfm, 
      count=self.__INITIAL_SCROBBLE_HISTORY_COUNT
    )
    fetch_recent_scrobbles_task.finished.connect(self.__handle_recent_scrobbles_fetched)
    QtCore.QThreadPool.globalInstance().start(fetch_recent_scrobbles_task)
    
  @QtCore.Slot(int)
  def toggleLastfmIsLoved(self, scrobble_index: int) -> None:
    
    if not self.__is_enabled:
      return

    scrobble = None

    if scrobble_index == HistoryViewModel.__CURRENT_SCROBBLE_INDEX:
      scrobble = self.__current_scrobble
    else:
      scrobble = self.scrobble_history[scrobble_index]

    new_value = not scrobble.lastfm_track.is_loved
    scrobble.lastfm_track.is_loved = new_value
    
    # Update any matching scrobbles in history
    for history_scrobble in self.scrobble_history:
      if history_scrobble == scrobble:
        history_scrobble.lastfm_track.is_loved = new_value
    
    # Update UI to reflect changes
    self.__emit_scrobble_ui_update_signals(scrobble)
    
    # Submit new value to Last.fm
    QtCore.QThreadPool.globalInstance().start(
      UpdateTrackLoveOnLastfm(
        lastfm=self.__application_reference.lastfm,
        scrobble=scrobble,
        value=new_value
      )
    )

  @QtCore.Slot(str)
  def switchToMediaPlugin(self, media_plugin_name: str) -> None:
    # Fake stopped event to un-load the current scrobble
    self.__handle_media_player_stopped()

    # Reset scrobble percentage
    self.__current_scrobble_percentage = 0

    # Disconnect event signals
    if self.__media_player:
      self.__media_player.stopped.disconnect(self.__handle_media_player_stopped)
      self.__media_player.playing.disconnect(self.__handle_media_player_playing)
      self.__media_player.paused.disconnect(self.__handle_media_player_paused)

    if media_plugin_name == 'spotify':
      self.__media_player = self.__spotify_plugin
    elif media_plugin_name == 'musicApp':
      self.__media_player = self.__music_app_plugin

    self.__set_is_scrobble_submission_enabled(self.__media_player.IS_SUBMISSION_ENABLED)
    logger.success(f'Switched media player to {self.__media_player.MEDIA_PLAYER_NAME}')

    # Reconnect event signals
    self.__media_player.stopped.connect(self.__handle_media_player_stopped)
    self.__media_player.playing.connect(self.__handle_media_player_playing)
    self.__media_player.paused.connect(self.__handle_media_player_paused)

    # Load initial track from newly selected media player without a notification
    if self.__media_player.is_open() and self.__is_enabled:
      # Avoid making an AppleScript request if the app isn't running (if we do, the app will launch)
      self.__media_player.request_initial_state()
    
    # Update 'Listening on X'  text in history view for current scrobble
    self.media_player_name_changed.emit()

  @QtCore.Slot(str)
  def mock_event(self, event_name):
    '''Allow mock player events to be triggered from QML'''

    self.__media_player.mock_event(event_name)

  # --- Private Methods ---

  def __handle_recent_scrobbles_fetched(self, recent_scrobbles: LastfmList[LastfmScrobble]):
    # Tell the history list model that we are going to change the data it relies on
    self.begin_refresh_history.emit()

    # Convert scrobbles from history into scrobble objects
    for i, recent_scrobble in enumerate(recent_scrobbles.items):
      self.scrobble_history.append(Scrobble.from_lastfm_scrobble(recent_scrobble))

      self.__load_external_scrobble_data(self.scrobble_history[i])

    self.end_refresh_history.emit()

  def __load_external_scrobble_data(self, scrobble: Scrobble) -> None:
    load_external_scrobble_data_task = LoadExternalScrobbleData(
      lastfm=self.__application_reference.lastfm,
      art_provider=self.__application_reference.art_provider,
      scrobble=scrobble
    )
    load_external_scrobble_data_task.update_ui_for_scrobble.connect(
      self.__emit_scrobble_ui_update_signals
    )
    load_external_scrobble_data_task.finished.connect(
      self.__handle_recent_scrobble_external_data_loaded
    )
    QtCore.QThreadPool.globalInstance().start(load_external_scrobble_data_task)

  def __handle_recent_scrobble_external_data_loaded(self) -> None:
    if not self.__is_enabled:
      return

    self.__scrobbles_with_external_data_count += 1

    if self.__scrobbles_with_external_data_count == len(self.scrobble_history): # Don't use initial scrobble count because there might not be that many
      # All scrobbles have loaded their additional data
      self.__should_show_loading_indicator = False
      self.should_show_loading_indicator_changed.emit()
      self.end_refresh_history.emit()

  def __emit_scrobble_ui_update_signals(self, scrobble: Scrobble) -> None:
    if not self.__is_enabled:
      return
    
    # Update details view if needed (all external scrobble data)
    if scrobble == self.selected_scrobble:
      self.selected_scrobble_changed.emit()
    
    # Update current scrobble view if needed (album art, is_loved)
    if scrobble == self.__current_scrobble:
      self.current_scrobble_data_changed.emit()
    
    # Update loved status and album art for all applicable history items if they match
    for i, history_scrobble in enumerate(self.scrobble_history):
      if scrobble == history_scrobble:
        self.scrobble_album_image_changed.emit(i)
        self.scrobble_lastfm_is_loved_changed.emit(i)

  def __submit_scrobble(self, scrobble: Scrobble) -> None:
    '''Add a scrobble object to the history array and submit it to Last.fm'''
    
    if not self.__is_enabled:
      return
    
    # Tell scrobble history list model that a change will be made
    self.pre_append_scrobble.emit()

    # Prepend the new scrobble to the scrobble_history array in the view model
    self.scrobble_history.insert(0, scrobble)

    # Tell scrobble history list model that a change was made in the view model
    # The list model will call the data function in the background to get the new data
    self.post_append_scrobble.emit()

    if self.__selected_scrobble_index:
      # Shift down the selected scrobble index if new scrobble has been added to the top
      # This is because if the user has a scrobble in the history selected and a new scrobble is submitted, it will display the wrong data if the index isn't updated
      # Change __selected_scrobble_index instead of calling set___selected_scrobble_index because the selected scrobble shouldn't be redundantly set to itself and still emit selected_scrobble_changed (wasting resources)
      if self.__selected_scrobble_index > HistoryViewModel.__CURRENT_SCROBBLE_INDEX:
        # Shift down the selected scrobble index by 1
        self.__selected_scrobble_index += 1

        # Tell the UI that the selected index changed, so it can update the selection highlight in the sidebar to the correct index
        self.selected_scrobble_index_changed.emit()

    # Submit scrobble to Last.fm
    if self.__is_submission_enabled:
      submit_scrobble_task = SubmitScrobble(
        lastfm=self.__application_reference.lastfm,
        scrobble=self.__current_scrobble
      )
      QtCore.QThreadPool.globalInstance().start(submit_scrobble_task)

    # Update playcounts for scrobbles (including the one just added to history)
    for history_scrobble in self.scrobble_history:
      if history_scrobble.lastfm_track:
        if history_scrobble.lastfm_track == scrobble.lastfm_track:
          history_scrobble.lastfm_track.plays += 1
      
      if history_scrobble.lastfm_artist:
        if history_scrobble.lastfm_artist == scrobble.lastfm_artist:
          history_scrobble.lastfm_artist.plays += 1

    # Reset flag so new scrobble can later be submitted
    self.__should_submit_current_scrobble = False

  def __update_current_scrobble(self, media_player_state: MediaPlayerState) -> None:
    '''Replace the current scrobble, update cached track start/finish, update the UI'''

    # if not self.__is_enabled:
    #   return

    logger.debug(f'Now playing: {media_player_state.artist_name} - {media_player_state.track_title} | {media_player_state.album_title}')
    
    # Initialize a new Scrobble object with the updated media player state
    self.__current_scrobble = Scrobble(
      artist_name=media_player_state.artist_name,
      track_title=media_player_state.track_title,
      album_title=media_player_state.album_title,
      timestamp=datetime.now()
    )

    # Update UI content in current scrobble sidebar item
    self.current_scrobble_data_changed.emit()

    # Reset player position to temporary value until a new value can be recieved from the media player
    self.__furthest_player_position_reached = 0

    # Refresh selected_scrobble with new __current_scrobble object if the current scrobble is selected, because otherwise the selected scrobble will reflect old data
    if self.__selected_scrobble_index == HistoryViewModel.__CURRENT_SCROBBLE_INDEX:
      self.selected_scrobble = self.__current_scrobble

      # Update details pane view
      self.selected_scrobble_changed.emit()
    elif self.__selected_scrobble_index is None:
      self.__selected_scrobble_index = HistoryViewModel.__CURRENT_SCROBBLE_INDEX
      self.selected_scrobble = self.__current_scrobble
      
      # Update the current scrobble highlight and song details pane views
      self.selected_scrobble_index_changed.emit()

      # Update details pane view
      self.selected_scrobble_changed.emit()

    # Update cached media player track playback data
    self.__current_track_crop = media_player_state.track_crop

    # Load Last.fm data and album art
    self.__load_external_scrobble_data(self.__current_scrobble)

  def __fetch_new_media_player_position(self) -> None:
    '''Fetch the current player position timestamp from the selected media player'''
    
    if (
      not self.__is_enabled

      # Skip fetching if there isn't a track playing
      or not self.__current_scrobble
    ):
      return

    fetch_player_position_task = FetchPlayerPosition(self.__media_player)
    fetch_player_position_task.finished.connect(self.__handle_player_position_fetched)
    QtCore.QThreadPool.globalInstance().start(fetch_player_position_task)

  def __handle_player_position_fetched(self, player_position: float) -> None:
    '''Update furthest player position reached if needed based on player position data'''
    
    if not self.__is_enabled:
      return
    
    # Only update the furthest reached position in the track if it's further than the last recorded furthest position
    # This is because if the user scrubs backward in the track, the scrobble progress bar will stop moving until they reach the previous furthest point reached in the track
    # TODO: Add support for different scrobble submission styles such as counting seconds of playback
    if player_position >= self.__furthest_player_position_reached:
      self.__furthest_player_position_reached = player_position
    
    # Count how many ticks have passed since the playback position changed (used for Discord RPC)
    if player_position == self.__cached_playback_position:
      self.__ticks_since_position_change += 1

      # Clear discord status if paused for more than 60 seconds
      if self.__ticks_since_position_change > 60 and self.__is_discord_rpc_enabled:
        # Skip next check since they have a cost
        if helpers.is_discord_open():
          self.__discord_rpc.clear()
    else:
      self.__ticks_since_position_change = 0
    
    self.__cached_playback_position = player_position
    self.__current_scrobble_percentage = self.__determine_current_scrobble_percentage()
    self.scrobble_percentage_changed.emit()

  def __determine_current_scrobble_percentage(self) -> int:
    '''Determine the percentage of the track that has played'''

    if not self.__is_enabled or not self.__current_scrobble:
      return 0

    # Skip calculations if the track has already reached the scrobble threshold
    if self.__should_submit_current_scrobble:
      return 1

    # Compensate for custom track start and end times
    # TODO: Only do this if the media player is the mac Music app
    relative_position = self.__furthest_player_position_reached - self.__current_track_crop.start
    relative_track_length = self.__current_track_crop.finish - self.__current_track_crop.start
    min_scrobble_length = relative_track_length * 0.75 # TODO: Grab the percentage from the settings database
    
    # Prevent scenarios where the relative position is negative
    relative_position = max(0, relative_position)
    scrobble_percentage = relative_position / min_scrobble_length

    # Prevent scenarios where the relative player position is greater than the relative track length (don't let the percentage by greater than 1)
    scrobble_percentage = min(scrobble_percentage, 1)

    # Submit current scrobble if the progress towards the scrobble threshold is 100%
    if scrobble_percentage == 1:
      self.__should_submit_current_scrobble = True

    return scrobble_percentage

  def __set_is_scrobble_submission_enabled(self, value: bool) -> None:
    # Ignore any changes to is_submission_enabled if it's disabled globally
    if os.environ.get('DISABLE_SUBMISSION'):
      self.__is_submission_enabled = False
    else:
      self.__is_submission_enabled = value

    logger.info(f'Scrobble submission is set to {self.__is_submission_enabled}')

  def __handle_media_player_stopped(self) -> None:
    '''Handle media player stop event (no track is loaded)'''

    if (
      not self.__is_enabled
      
      # Don't do anything this case if there was nothing playing previously
      or not self.__current_scrobble
    ):
      return

    if self.__is_discord_rpc_enabled and helpers.is_discord_open():
      self.__discord_rpc.clear()
    
    # Submit if the music player stops as well, not just when a new track starts
    if self.__should_submit_current_scrobble:
      self.__submit_scrobble(self.__current_scrobble)

    # Reset current scrobble
    self.__current_scrobble = None

    # Update the UI in current scrobble sidebar item
    self.current_scrobble_data_changed.emit()

    # If the current scrobble is selected, deselect it
    if self.__selected_scrobble_index == HistoryViewModel.__CURRENT_SCROBBLE_INDEX:
      self.__selected_scrobble_index = None
      self.selected_scrobble = None
      
      # Update the current scrobble highlight and song details pane views
      self.selected_scrobble_index_changed.emit()
      self.selected_scrobble_changed.emit()

  def __handle_media_player_playing(self, media_player_state: MediaPlayerState) -> None:
    '''Handle media player play event'''

    # if not self.__is_enabled:
    #   return

    # Update now playing on Last.fm
    if self.__is_submission_enabled:
      QtCore.QThreadPool.globalInstance().start(
        UpdateNowPlaying(
          lastfm=self.__application_reference.lastfm, 
          artist_name=media_player_state.artist_name,
          track_title=media_player_state.track_title,
          album_title=media_player_state.album_title,
          duration=media_player_state.track_crop.finish - media_player_state.track_crop.start
        )
      )

    # Update Discord rich presence
    if self.__is_discord_rpc_enabled and helpers.is_discord_open():
      self.__discord_rpc.update(
        details=media_player_state.track_title,
        state=media_player_state.artist_name + (
          (
            ' | ' + media_player_state.album_title
          ) if media_player_state.album_title else ''
        ),
        large_image='music-logo',
        large_text='Playing on Music',
        small_image='lastredux-logo',
        small_text='Scrobbling on LastRedux',
        start=(datetime.now() - timedelta(seconds=media_player_state.position)).timestamp() # Don't include track start to accurately reflect timestamp in uncropped track
      )
    
    # Update playback indicator
    self.is_player_paused = False
    self.is_player_paused_changed.emit()

    current_track_changed = (
      not self.__current_scrobble
      or not self.__current_scrobble.is_equal_to_media_player_state(media_player_state)
    )

    # Only run this code when the track changes (or the first track is loaded)
    if current_track_changed:
      # Submit the previous track when the current track changes if it hit the scrobbling threshold
      if self.__should_submit_current_scrobble:
        self.__submit_scrobble(self.__current_scrobble)

      self.__update_current_scrobble(media_player_state)
  
  def __handle_media_player_paused(self, media_player_state: MediaPlayerState) -> None:
    '''Handle media player pause event'''

    # Update playback indicator
    self.is_player_paused = True
    self.is_player_paused_changed.emit()

    # Load scrobble if it's new
    if not self.__current_scrobble:
      self.__update_current_scrobble(media_player_state)

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

  currentScrobble = QtCore.Property(
    type='QVariant',
    fget=lambda self: asdict(self.__current_scrobble) if self.__current_scrobble else None,
    notify=current_scrobble_data_changed
  )

  scrobblePercentage = QtCore.Property(
    type=float,
    fget=lambda self: self.__current_scrobble_percentage,
    notify=scrobble_percentage_changed
  )

  isSpotifyPluginAvailable = QtCore.Property(
    type=bool,
    fget=lambda self: self.__is_spotify_plugin_available,
    notify=is_spotify_plugin_available_changed
  )

  isUsingMockPlayer = QtCore.Property(
    type=bool,
    fget=lambda self: isinstance(self.__media_player, MockPlayerPlugin),
    notify=is_using_mock_player_changed
  )

  selectedScrobbleIndex = QtCore.Property(
    type=int,
    fget=get_selected_scrobble_index,
    fset=set_selected_scrobble_index,
    notify=selected_scrobble_index_changed
  )

  shouldShowLoadingIndicator = QtCore.Property(
    type=bool,
    fget=lambda self: self.__should_show_loading_indicator,
    notify=should_show_loading_indicator_changed
  )

  mediaPlayerName = QtCore.Property(
    type=str,
    fget=lambda self: self.__media_player.MEDIA_PLAYER_NAME,
    notify=media_player_name_changed
  )