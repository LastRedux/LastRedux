from typing import Dict

from PySide2 import QtCore
from ScriptingBridge import SBApplication
from Foundation import NSDistributedNotificationCenter
from loguru import logger

from datatypes.MediaPlayerState import MediaPlayerState

class FetchTrackCrop(QtCore.QObject, QtCore.QRunnable):
  finished = QtCore.Signal(dict)

  def __init__(self, applescript_music_app):
    '''Use AppleScript to fetch the current track's start and finish timestamps (This often fails and returns 0.0 for both)'''

    QtCore.QObject.__init__(self)
    QtCore.QRunnable.__init__(self)
    self.__applescript_music_app = applescript_music_app
    self.setAutoDelete(True)

  def run(self):
    current_track = self.__applescript_music_app.currentTrack()

    self.finished.emit({
      'track_start': current_track.start(),
      'track_finish': current_track.finish()
    })

class MusicAppPlugin(QtCore.QObject):
  PLAYING_STATE = 1800426320 # From Music.app BridgeSupport enum definitions

  # Media player signals
  stopped = QtCore.Signal()
  paused = QtCore.Signal(MediaPlayerState)
  playing = QtCore.Signal(MediaPlayerState)

  # Music app signals
  does_not_have_artist_error = QtCore.Signal()

  def __init__(self):
    QtCore.QObject.__init__(self)

    # Store the current media player state
    self.__state: MediaPlayerState = None

    # Store reference to Music app in AppleScript
    self.__applescript_music_app = SBApplication.applicationWithBundleIdentifier_('com.apple.Music')

    # Set up NSNotificationCenter (refer to https://lethain.com/how-to-use-selectors-in-pyobjc)
    self.__default_center = NSDistributedNotificationCenter.defaultCenter()
    self.__default_center.addObserver_selector_name_object_(self, '__handleNotificationFromMusic:', 'com.apple.Music.playerInfo', None)

    # Store the latest notification from NSNotificationObserver
    self.__cached_notification_payload = None

    # Load currently playing song if there is one
    if self.is_open():
      # Only load current track if something is already playing
      if self.__applescript_music_app.playerState() == MusicAppPlugin.PLAYING_STATE:
        self.load_track_with_applescript()

  def __str__(self):
    return 'Music'

  # --- Media Player Implementation ---

  def get_player_position(self) -> float:
    '''Use AppleScript to fetch the current Music app playback position'''

    return self.__applescript_music_app.playerPosition()

  def is_open(self):
    return self.__applescript_music_app.isRunning()

  def load_track_with_applescript(self):
    current_track = self.__applescript_music_app.currentTrack()
    track_title = current_track.name()
    
    if not track_title:
      # User is playing a non-library track, so we force a play notification
      self.__applescript_music_app.pause()
      self.__applescript_music_app.playpause() # There is no play function for whatever reason
      return

    self.__state = MediaPlayerState.build_from_applescript_track(current_track, self.__applescript_music_app.playerState() == MusicAppPlugin.PLAYING_STATE)
    
    # Wait 1 second for the HistoryViewModel to load before sending initial playing signal
    timer = QtCore.QTimer(self)
    timer.setSingleShot(True) # Single-shot timer, basically setTimeout from JS
    timer.timeout.connect(lambda: self.playing.emit(self.__state) if self.__state.is_playing else self.paused.emit(self.__state))
    timer.start(1000)

  # --- Private Methods ---

  def __handleNotificationFromMusic_(self, notification):
    '''Handle Objective-C notifications for Music app events'''

    self.__cached_notification_payload = notification.userInfo()
    player_state = self.__cached_notification_payload['Player State']

    if player_state == 'Stopped':
      self.stopped.emit()
      return
    
    track_title = self.__cached_notification_payload.get('Name')

    # Ignore notification if there's no track title (Usually happens with radio stations)
    if not track_title:
      return

    # Apple Music puts Connecting... state string in the track title field for some reason
    if track_title == 'Connecting…': # TODO: Find way to check this that works with other languages
      # Connecting... state should remove track from details pane and deselect it, so we're pretending the player is stopped
      self.stopped.emit()
      return

    artist_name = self.__cached_notification_payload.get('Artist')

    # Some tracks don't have an artist and can't be scrobbled on Last.fm
    if not artist_name:
      self.does_not_have_artist_error.emit()
      self.stopped.emit()
      return

    is_playing = player_state == 'Playing'

    # Detect if paused to emit paused signal without running AppleScript again
    # Make sure that we have track data first
    if self.__state and not is_playing:
      self.paused.emit(self.__state)
      return
    
    album_title = self.__cached_notification_payload.get('Album', '')
    
    # Emit play signal early and skip AppleScript if the track is the same as the last one (if it exists)
    if self.__state:
      if self.__state.track_title == track_title and self.__state.artist_name == artist_name and self.__state.album_title == album_title and self.__state.track_finish: # Check for track_finish so playing isn't emitted prematurely if track is play cycled repeatedly before AppleScript request can complete
        self.playing.emit(self.__state)
        return
    
    # Create new state object to store new track data
    self.__state = MediaPlayerState(is_playing, track_title, artist_name, album_title)
    
    # Fetch track crop data (start and finish timestamps)
    # Delay for 100ms to give enough time for AppleScript to update with new current track (Sometimes, AppleScript lags behind the notifications)
    timer = QtCore.QTimer(self)
    timer.setSingleShot(True) # Single-shot timer, basically setTimeout from JS
    timer.timeout.connect(self.__launch_fetch_track_crop_task)
    timer.start(100)

  def __launch_fetch_track_crop_task(self):
    get_library_track_crop = FetchTrackCrop(self.__applescript_music_app)
    get_library_track_crop.finished.connect(self.__handle_completion_of_get_track_crop_request)
    QtCore.QThreadPool.globalInstance().start(get_library_track_crop)
  
  def __handle_completion_of_get_track_crop_request(self, track_crop):
    '''Figure out what to do with the results of the track crop request'''

    if track_crop['track_finish'] != 0:
      # A track finish was found, so we can use the actual crop values
      self.__state.track_start = track_crop['track_start']
      self.__state.track_finish = track_crop['track_finish']
    else:
      # No track finish was found (most likely a non-library track), we'll use the total duration as the track finish instead
      total_time = self.__cached_notification_payload.get('Total Time')

      if not total_time:
        # Sometimes even this fails, there's nothing we can do
        # TODO: Alert the user to the fact that their track can't be scrobbled
        logger.error(f'Error getting track duration for {self.__cached_notification_payload}')

      self.__state.track_finish = total_time / 1000 # Convert from ms to s
    
    # Finally emit play/pause signal
    if self.__state.is_playing:
      self.playing.emit(self.__state)
    else:
      self.paused.emit(self.__state)