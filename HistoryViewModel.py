from dataclasses import is_dataclass
import os
from datetime import datetime
from plugins.MusicAppPlugin import MusicAppPlugin

from loguru import logger
from PySide2 import QtCore
from ScriptingBridge import SBApplication

from ApplicationViewModel import ApplicationViewModel

from ApplicationViewModel import ApplicationViewModel

from plugins.MockPlayerPlugin import MockPlayerPlugin
from plugins.SpotifyPlugin import SpotifyPlugin
from datatypes.Scrobble import Scrobble
from tasks.FetchPlayerPosition import FetchPlayerPosition
from tasks.LoadAdditionalScrobbleDataTask import LoadAdditionalScrobbleDataTask
from tasks.SubmitTrackIsLovedChanged import SubmitTrackIsLovedChanged
from tasks.FetchRecentScrobblesTask import FetchRecentScrobblesTask
from tasks.SubmitScrobbleTask import SubmitScrobbleTask
from tasks.UpdateNowPlayingTask import UpdateNowPlayingTask
import util.LastfmApiWrapper as lastfm

class HistoryViewModel(QtCore.QObject):
  # Constants
  __INITIAL_SCROBBLE_HISTORY_COUNT = int(os.environ.get('INITIAL_HISTORY_ITEMS', 30)) # 30 is the default but can be configured

  # Qt Property changed signals
  is_enabled_changed = QtCore.Signal()
  current_scrobble_data_changed = QtCore.Signal()
  current_scrobble_percentage_changed = QtCore.Signal()
  is_using_mock_player_plugin_changed = QtCore.Signal()
  is_in_mini_mode_changed = QtCore.Signal()
  is_player_paused_changed = QtCore.Signal()
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

  showNotification = QtCore.Signal(str, str)

  def initialize_variables(self):
    # Store Scrobble objects that have been submitted
    self.scrobble_history = []

    # Keep track of whether the history view is loading data
    self.__should_show_loading_indicator = False

    # Keep track of how many scrobbles have their additional data loaded from Last.fm and Spotify
    self.__scrobbles_with_additional_data_count = 0

    # Hold a Scrobble object for currently playing track (will later be submitted)
    self.__current_scrobble = None
    
    # Hold the index of the selected scrobble in the sidebar
    self.__selected_scrobble_index = None # -1 for current scrobble, None for no scrobble, numbers > 0 for history items
    
    # Hold the Scrobble object at the __selected_scrobble_index
    # This can either be a copy of the current scrobble or one in the history
    self.selected_scrobble = None

    # Keep track of whether the current scrobble has hit the threshold for scrobbling (to submit when current track changes)
    self.__current_scrobble_percentage = 0
    self.__should_submit_current_scrobble = None
    
    # Keep track of furthest position reached in a song to allow moving back without losing progress
    self.__furthest_player_position_reached = None

    # Keep track of the current track's start and finish timestamps since it isn't saved to the scrobble object
    self.__current_track_start = None
    self.__current_track_finish = None

  def __init__(self):
    QtCore.QObject.__init__(self)

    self.__application_reference = None
    self.__is_enabled = False
    
    # Initialize media player plugins
    self.__spotify_plugin = SpotifyPlugin()
    self.__music_app_plugin = MusicAppPlugin()
    self.media_player = None
    self.is_submission_enabled = None
    
    if os.environ.get('MOCK'):
      self.media_player = MockPlayerPlugin()
    else:
      use_spotify = False
      spotify_app = SBApplication.applicationWithBundleIdentifier_('com.spotify.client')
      
      # TODO: Use better method to figure out if Spotify is installed without logged error
      if spotify_app:
        if spotify_app.isRunning():
          use_spotify = True
      
      if use_spotify:
        self.media_player = self.__spotify_plugin
        self.set_is_scrobble_submission_enabled(False)
      else:
        # Use Music app plugin in all other cases since every Mac has it
        self.media_player = self.__music_app_plugin
        self.set_is_scrobble_submission_enabled(True)

    self.media_player.stopped.connect(self.__handle_media_player_stopped)
    self.media_player.playing.connect(self.__handle_media_player_playing)
    self.media_player.paused.connect(self.__handle_media_player_paused)

    # Get instance of lastfm api wrapper
    self.lastfm_instance = lastfm.get_static_instance()
    
    # TODO: Move these properties to an App view model
    self.is_in_mini_mode = False
    self.is_player_paused = False
    
    self.initialize_variables()

    # Start polling interval to check for new media player position
    self.__timer = QtCore.QTimer(self)
    self.__timer.timeout.connect(self.__fetch_new_media_player_position)


  def set_is_scrobble_submission_enabled(self, value: bool):
    if not os.environ.get('DISABLE_SUBMISSION'):
      self.is_submission_enabled = value

    if self.is_submission_enabled:
      logger.debug('Scrobble submission is enabled')
    else:
      logger.debug('Scrobble submission is disabled')

  # --- Qt Property Getters and Setters ---

  def set_application_reference(self, new_reference):
    if new_reference:
      self.__application_reference = new_reference

      self.__application_reference.is_logged_in_changed.connect(lambda: self.set_is_enabled(self.__application_reference.is_logged_in))

  def get_current_scrobble_data(self):
    '''Return data about the currently playing track in the active media player'''
    
    if self.__is_enabled and self.__current_scrobble:
      return {
        'hasLastfmData': self.__current_scrobble.loading_state == 'LASTFM_TRACK_LOADED',
        'trackTitle': self.__current_scrobble.title,
        'artistName': self.__current_scrobble.artist.name,
        'lastfmIsLoved': self.__current_scrobble.lastfm_is_loved,
        'albumImageUrl': self.__current_scrobble.album.image_url_small # The scrobble history album arts are small so we don't want to render the full size art
      }
    
    # Return None if there isn't a current scrobble (such as when the app is first loaded or if there is no track playing)
    return None

  def get_current_scrobble_percentage(self):
    return self.__current_scrobble_percentage if self.__is_enabled else 0
  
  def get_is_using_mock_player_plugin(self):
    return isinstance(self.media_player, MockPlayerPlugin)
    
  def get_selected_scrobble_index(self):
    '''Make the private selected scrobble index variable available to the UI'''
    
    if self.__selected_scrobble_index is None:
      # -2 represents no selection because Qt doesn't understand Python's None value
      return -2

    return self.__selected_scrobble_index
  
  def set_selected_scrobble_index(self, new_index):
    if self.__is_enabled:
      # Prevent setting an illegal index with keyboard shortcuts
      if (
        new_index == len(self.scrobble_history) # Prevent navigating past scrobble history
        or new_index == -2 # Prevent navigating into negative numbers
        or self.__current_scrobble is None and new_index == -1 # Prevent navigating to current scrobble when there isn't one
      ):
        return
      
      self.__selected_scrobble_index = new_index

      # Tell the UI that the selected index changed, so it can update the selection highlight in the sidebar to the correct index
      self.selected_scrobble_index_changed.emit()

      # Update selected_scrobble (Scrobble type) according to the new index
      if new_index == -1: # If the new selection is the current scrobble
        self.selected_scrobble = self.__current_scrobble
      else:
        self.selected_scrobble = self.scrobble_history[new_index]

        # Load additional scrobble data if it isn't already present
        self.__load_additional_scrobble_data(self.selected_scrobble)
      
      # Tell the UI that the selected scrobble was changed, so views like the scrobble details pane can update accordingly
      self.selected_scrobble_changed.emit()

  def get_is_enabled(self): # Function instead of lambda because DetailsViewModel uses this
    return self.__is_enabled

  def set_is_enabled(self, is_enabled):
    self.__is_enabled = is_enabled
    self.is_enabled_changed.emit()

    if is_enabled:
      self.initialize_variables()
      self.media_player.request_initial_state()
      polling_interval = 100 if os.environ.get('MOCK') else 1000
      self.__timer.start(polling_interval)

      # Load in recent scrobbles from Last.fm and process them
      if self.__INITIAL_SCROBBLE_HISTORY_COUNT > 0:
        self.reloadHistory()
    else:
      self.begin_refresh_history.emit()
      self.initialize_variables()
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

    if self.__is_enabled and not self.__should_show_loading_indicator:
      logger.trace('Reloading scrobble history from Last.fm')

      # Update loading indicator
      self.__should_show_loading_indicator = True
      self.should_show_loading_indicator_changed.emit()

      # Reset scrobble history list
      self.begin_refresh_history.emit()
      self.scrobble_history = []
      self.end_refresh_history.emit()
      self.__scrobbles_with_additional_data_count = 0

      # Fetch and load recent scrobbles
      fetch_recent_scrobbles_task = FetchRecentScrobblesTask(self.lastfm_instance, self.__INITIAL_SCROBBLE_HISTORY_COUNT)
      fetch_recent_scrobbles_task.finished.connect(self.__process_fetched_recent_scrobbles)
      QtCore.QThreadPool.globalInstance().start(fetch_recent_scrobbles_task)
    
  @QtCore.Slot(int)
  def toggleLastfmIsLoved(self, index):
    if self.__is_enabled:
      scrobble = None

      # -1 refers to current scrobble
      if index == -1:
        scrobble = self.__current_scrobble
      else:
        scrobble = self.scrobble_history[index]

      if scrobble.loading_state == 'LASTFM_TRACK_NOT_FOUND':
        return
      
      new_is_loved = not scrobble.lastfm_is_loved

      if index == -1:
        scrobble.lastfm_is_loved = new_is_loved
      
      # Update any scrobbles in the scrobble history array that match the scrobble that changed
      for history_item in self.scrobble_history:
        if scrobble.equals(history_item):
          history_item.lastfm_is_loved = new_is_loved
      
      # If hearting song in history, also update current scrobble state
      if index != -1 and scrobble.equals(self.__current_scrobble):
        self.__current_scrobble.lastfm_is_loved = new_is_loved

      self.__emit_scrobble_ui_update_signals(scrobble)
      
      # Tell Last.fm about our new is_loved value
      submit_track_is_loved_task = SubmitTrackIsLovedChanged(self.lastfm_instance, scrobble, new_is_loved)
      QtCore.QThreadPool.globalInstance().start(submit_track_is_loved_task)

  @QtCore.Slot()
  def toggleMiniMode(self):
    if self.__is_enabled:
      self.is_in_mini_mode = not self.is_in_mini_mode
      self.is_in_mini_mode_changed.emit()

  @QtCore.Slot(str)
  def switchToMediaPlugin(self, media_plugin_name):
    # Fake stopped event to unload the current scrobble
    self.__handle_media_player_stopped()

    # Disconnect event signals
    self.media_player.stopped.disconnect(self.__handle_media_player_stopped)
    self.media_player.playing.disconnect(self.__handle_media_player_playing)
    self.media_player.paused.disconnect(self.__handle_media_player_paused)

    if media_plugin_name == 'spotify':
      self.media_player = self.__spotify_plugin
      self.set_is_scrobble_submission_enabled(False)
      logger.success('Switched media player to Spotify')
    elif media_plugin_name == 'musicApp':
      self.media_player = self.__music_app_plugin
      self.set_is_scrobble_submission_enabled(True)
      logger.success('Switched media player to Music app')

    # Reconnect event signals
    self.media_player.stopped.connect(self.__handle_media_player_stopped)
    self.media_player.playing.connect(self.__handle_media_player_playing)
    self.media_player.paused.connect(self.__handle_media_player_paused)

    # Load initial track from newly selected media player without a notification
    if self.media_player.is_open():
      # Avoid making an AppleScript request if the app isn't running (if we do, the app will launch)
      self.media_player.request_initial_state()
    
    # Update 'Listening on X'  text in history view for current scrobble
    self.media_player_name_changed.emit()

  @QtCore.Slot(str)
  def mock_event(self, event_name):
    self.media_player.mock_event(event_name)

  # --- Private Functions ---

  def __submit_scrobble(self, scrobble):
    '''Add a scrobble object to the history array and submit it to Last.fm'''
    
    if self.__is_enabled:
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
        if self.__selected_scrobble_index > -1: # > -1 is the same as not -2 (no scrobble selected) and not -1
          # Shift down the selected scrobble index by 1
          self.__selected_scrobble_index += 1

          # Tell the UI that the selected index changed, so it can update the selection highlight in the sidebar to the correct index
          self.selected_scrobble_index_changed.emit()

      # Submit scrobble to Last.fm in background thread task
      if self.is_submission_enabled:
        submit_scrobble_task = SubmitScrobbleTask(self.lastfm_instance, self.__current_scrobble)
        QtCore.QThreadPool.globalInstance().start(submit_scrobble_task)

      # TODO: Decide what happens when a scrobble that hasn't been fully downloaded is submitted. Does it wait for the data to load for the plays to be updated or should it not submit at all?
      if scrobble.loading_state == 'LASTFM_TRACK_LOADED':
        scrobble.lastfm_plays += 1
        scrobble.artist.lastfm_plays += 1

        # Refresh scrobble details pane if the submitted scrobble is selected
        if self.selected_scrobble == scrobble:
          self.selected_scrobble_changed.emit()

      # Reset flag so new scrobble can later be submitted
      self.__should_submit_current_scrobble = False

  @QtCore.Slot(list)
  def __process_fetched_recent_scrobbles(self, lastfm_recent_scrobbles):
    # Tell the history list model that we are going to change the data it relies on
    self.begin_refresh_history.emit()

    for lastfm_scrobble in lastfm_recent_scrobbles:
      # Don't include currently playing track to scrobble history
      if lastfm_scrobble.get('@attr') and lastfm_scrobble.get('@attr').get('nowplaying'):
        continue

      scrobble = Scrobble(
        lastfm_scrobble['name'], 
        lastfm_scrobble['artist']['name'], 
        lastfm_scrobble['album']['#text'], 
        datetime.fromtimestamp(int(lastfm_scrobble['date']['uts']))
      )
      
      self.scrobble_history.append(scrobble)
      self.__load_additional_scrobble_data(scrobble)

    # Tell the history list model that we finished changing the data it relies on
    self.end_refresh_history.emit()

  def __determine_current_scrobble_percentage(self):
    '''Determine the percentage of the track that has played compared to a user-set percentage of the track length'''

    if not self.__is_enabled or not self.__current_scrobble:
      return 0

    # Compensate for custom track start and end times
    # TODO: Only do this if the media player is the mac Music app
    relative_position = self.__furthest_player_position_reached - self.__current_track_start
    relative_track_length = self.__current_track_finish - self.__current_track_start
    min_scrobble_length = relative_track_length * 0.75 # TODO: Grab the percentage from the settings database
    
    # Prevent scenarios where the relative position is negative
    relative_position = max(0, relative_position)

    scrobble_percentage = relative_position / min_scrobble_length

    # Prevent scenarios where the relative player position is greater than the relative track length (don't let the percentage by greater than 1)
    scrobble_percentage = min(scrobble_percentage, 1)

    # Submit current scrobble if the scrobble percentage (progress towards the scrobble threshold) is 100%
    if not self.__should_submit_current_scrobble and scrobble_percentage == 1:
      # TODO: Only submit when the song changes or the app is closed
      self.__should_submit_current_scrobble = True
      logger.debug(f'{self.__current_scrobble.title}: Ready for submission to Last.fm')

    return scrobble_percentage

  def __update_scrobble_to_match_new_media_player_data(self, new_media_player_state):
    '''Set __current_scrobble to a new Scrobble object created from the currently playing track, update the playback data for track start/finish, and update the UI'''

    if self.__is_enabled:
      # Initialize a new Scrobble object with the currently playing track data
      # This will set the Scrobble's timestamp to the current date
      self.__current_scrobble = Scrobble(new_media_player_state.track_title, new_media_player_state.artist_name, new_media_player_state.album_title)

      logger.debug(f'Now playing: {new_media_player_state.artist_name} - {new_media_player_state.track_title} | {new_media_player_state.album_title}')

      # Update UI content in current scrobble sidebar item
      self.current_scrobble_data_changed.emit()

      # Tell Last.fm to update the user's now playing status
      if self.is_submission_enabled:
        QtCore.QThreadPool.globalInstance().start(UpdateNowPlayingTask(self.lastfm_instance, self.__current_scrobble))

      # Reset player position to temporary value until a new value can be recieved from the media player
      self.__furthest_player_position_reached = 0

      # Refresh selected_scrobble with new __current_scrobble object if the current scrobble is selected, because otherwise the selected scrobble will reflect old data
      if self.__selected_scrobble_index == -1:
        self.selected_scrobble = self.__current_scrobble

        # Update details pane view
        self.selected_scrobble_changed.emit()
      elif self.__selected_scrobble_index is None:
        self.__selected_scrobble_index = -1
        self.selected_scrobble = self.__current_scrobble
        
        # Update the current scrobble highlight and song details pane views
        self.selected_scrobble_index_changed.emit()

        # Update details pane view
        self.selected_scrobble_changed.emit()

      # Update cached media player track playback data
      self.__current_track_start = new_media_player_state.track_start
      self.__current_track_finish = new_media_player_state.track_finish

      logger.trace(f'New media player state: {new_media_player_state}')

      self.__load_additional_scrobble_data(self.__current_scrobble)

  def __load_additional_scrobble_data(self, scrobble):
    '''Create thread task to get additional info about track from Last.fm in the background'''

    if self.__is_enabled:
      load_additional_scrobble_data_task = LoadAdditionalScrobbleDataTask(self, scrobble)

      # Connect the emit_scrobble_ui_update_signals signal in the task to the local slot with the same name
      load_additional_scrobble_data_task.emit_scrobble_ui_update_signals.connect(self.__emit_scrobble_ui_update_signals)
      load_additional_scrobble_data_task.finished.connect(self.__recent_scrobbles_done_loading)

      # Add task to global thread pool and run
      QtCore.QThreadPool.globalInstance().start(load_additional_scrobble_data_task)

  def __recent_scrobbles_done_loading(self):
    if self.__is_enabled:
      self.__scrobbles_with_additional_data_count += 1

    if self.__scrobbles_with_additional_data_count == len(self.scrobble_history):
      self.__should_show_loading_indicator = False
      self.should_show_loading_indicator_changed.emit()

  def __emit_scrobble_ui_update_signals(self, scrobble):
    if self.__is_enabled:
      # Update scrobble data in details pane view if it's currently showing (when the selected scrobble is the one being updated)
      if scrobble.equals(self.selected_scrobble):
        self.selected_scrobble_changed.emit()
      
      # If scrobble is the current track, update current scrobble sidebar item to reflect actual is_loved status
      if scrobble.equals(self.__current_scrobble):
        self.current_scrobble_data_changed.emit()
      
      # Also update image of history item if scrobble is already in history (check every item for find index)
      for i, history_item in enumerate(self.scrobble_history):
        # TODO: Make separate signal that only updates is_loved data because the other data shown doesn't change
        if scrobble.equals(history_item):
          self.scrobble_album_image_changed.emit(i)
          self.scrobble_lastfm_is_loved_changed.emit(i)
          # No break just in case track is somehow scrobbled twice before image loads

  @QtCore.Slot()
  def __fetch_new_media_player_position(self):
    '''Fetch the current player position from the media player (timestamp that the user is at in the song)'''
    
    if self.__is_enabled:
      # Skip fetching if there isn't a track playing
      if self.__current_scrobble:
        # Create thread task with reference to the media player
        fetch_new_media_player_position = FetchPlayerPosition(self.media_player)

        # Process the new media player position after the data is returned
        fetch_new_media_player_position.finished.connect(self.__process_new_media_player_position)

        # Add task to global thread pool and run it
        QtCore.QThreadPool.globalInstance().start(fetch_new_media_player_position)

  def __process_new_media_player_position(self, player_position):
    '''Update furthest player position reached if appropriate based on the latest player position data'''
    
    if self.__is_enabled:
      # Only update the furthest reached position in the track if it's further than the last recorded furthest position
      # This is because if the user scrubs backward in the track, the scrobble progress bar will stop moving until they reach the previous furthest point reached in the track
      # TODO: Add support for different scrobble submission styles such as counting seconds of playback
      if player_position >= self.__furthest_player_position_reached:
        self.__furthest_player_position_reached = player_position
      
      self.__current_scrobble_percentage = self.__determine_current_scrobble_percentage()

      # Update scrobble progress bar UI
      self.current_scrobble_percentage_changed.emit()

  def __handle_media_player_stopped(self):
    '''Handle media player stop event (no track is loaded)'''

    if self.__is_enabled:
      # Only handle this case if there was something playing previously
      if self.__current_scrobble:
        # Submit if the music player stops as well, not just when a new track starts
        if self.__should_submit_current_scrobble:
          self.__submit_scrobble(self.__current_scrobble)

        self.__current_scrobble = None

        # Update the UI in current scrobble sidebar item
        self.current_scrobble_data_changed.emit()

        # If the current scrobble is selected, deselect it
        if self.__selected_scrobble_index == -1:
          self.__selected_scrobble_index = None
          self.selected_scrobble = None
          
          # Update the current scrobble highlight and song details pane views
          self.selected_scrobble_index_changed.emit()
          self.selected_scrobble_changed.emit()

  def __handle_media_player_playing(self, new_media_player_state):
    '''Handle media player play event'''

    if self.__is_enabled:
      # Update playback indicator
      self.is_player_paused = False
      self.is_player_paused_changed.emit()

      current_track_changed = not self.__current_scrobble or new_media_player_state.track_title != self.__current_scrobble.title or new_media_player_state.artist_name != self.__current_scrobble.artist.name or new_media_player_state.album_title != self.__current_scrobble.album.title

      # Only run this code when the track changes (or the first track is loaded)
      if current_track_changed:
        # with open('._now_playing.txt', 'w+') as f:
        #   f.write(f'{new_media_player_state.artist_name} - {new_media_player_state.track_title}')

        # Submit the previous track when the current track changes if it hit the scrobbling threshold
        if self.__should_submit_current_scrobble:
          self.__submit_scrobble(self.__current_scrobble)

        self.__update_scrobble_to_match_new_media_player_data(new_media_player_state)
  
  def __handle_media_player_paused(self, new_media_player_state):
    '''Handle media player pause event'''

    # Update playback indicator
    self.is_player_paused = True
    self.is_player_paused_changed.emit()

  # --- Qt Properties ---
  
  applicationReference = QtCore.Property(ApplicationViewModel, lambda self: self.__application_reference, set_application_reference)
  isEnabled = QtCore.Property(bool, get_is_enabled, set_is_enabled, notify=is_enabled_changed)
  currentScrobbleData = QtCore.Property('QVariant', get_current_scrobble_data, notify=current_scrobble_data_changed)
  currentScrobblePercentage = QtCore.Property(float, get_current_scrobble_percentage, notify=current_scrobble_percentage_changed)
  isUsingMockPlayerPlugin = QtCore.Property(bool, get_is_using_mock_player_plugin, notify=is_using_mock_player_plugin_changed)
  selectedScrobbleIndex = QtCore.Property(int, get_selected_scrobble_index, set_selected_scrobble_index, notify=selected_scrobble_index_changed)
  shouldShowLoadingIndicator = QtCore.Property(bool, lambda self: self.__should_show_loading_indicator, notify=should_show_loading_indicator_changed)
  mediaPlayerName = QtCore.Property(str, lambda self: self.media_player.__str__(), notify=media_player_name_changed)