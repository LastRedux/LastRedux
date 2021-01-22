from PySide2 import QtCore
from ScriptingBridge import SBApplication
from Foundation import NSDistributedNotificationCenter
from loguru import logger

from plugins.macOS.MacMediaPlayerPlugin import MacMediaPlayerPlugin
from datatypes.MediaPlayerState import MediaPlayerState
from datatypes.TrackCrop import TrackCrop
from .FetchTrackCrop import FetchTrackCrop

class MusicAppPlugin(MacMediaPlayerPlugin):
  MEDIA_PLAYER_NAME = 'Music'
  MEDIA_PLAYER_ID = 'musicApp'
  IS_SUBMISSION_ENABLED = True

  def __init__(self) -> None:
    # Store reference to Music app in AppleScript
    self.__applescript_app = SBApplication.applicationWithBundleIdentifier_('com.apple.Music')
    
    super().__init__(self.__applescript_app)

    # Set up NSNotificationCenter (refer to https://lethain.com/how-to-use-selectors-in-pyobjc)
    self.__default_center = NSDistributedNotificationCenter.defaultCenter()
    self.__default_center.addObserver_selector_name_object_(
      self,
      '__handleNotificationFromMusic:',
      'com.apple.Music.playerInfo',
      None
    )

    # Store the latest notification from NSNotificationObserver
    self.__cached_notification_payload: dict = None

    # Store latest state
    self.__state: MediaPlayerState = None

  # --- Mac Media Player Implementation ---

  def request_initial_state(self) -> None:
    # Avoid making an AppleScript request if the app isn't running (if we do, the app will launch)
    if not self.__applescript_app.isRunning():
      return

    is_playing = self.__applescript_app.playerState() == MusicAppPlugin.PLAYING_STATE

    if not is_playing:
      return

    track = self.__applescript_app.currentTrack()
    track_title = track.name()
    
    if not track_title:
      # User is playing a non-library track, so AppleScript can't see the data
      # Instead, we have to force a play notification
      self.__applescript_app.pause()
      self.__applescript_app.playpause() # There is no play function for whatever reason
      return

    self.__handle_new_state(
      MediaPlayerState(
        artist_name=track.artist(),
        track_title=track_title,
        album_title=track.album() or None, # Prevent storing empty strings in album_title key
        is_playing=True, # We can't differentiate between paused and stopped, so we will only send a new state if playing
        position=self.get_player_position()
      )
    )

  # --- Private Methods ---
    
  def __handle_new_state(self, new_state: MediaPlayerState) -> None:
    # Ignore notification if there's no track title (Usually happens with radio stations)
    if not new_state.track_title:
      return

    # Apple Music puts Connecting... state string in the track title field for some reason
    if new_state.track_title == 'Connecting…': # TODO: Find a better way to check that doesn't break other languages, songs named Connecting...
      self.stopped.emit()
      return

    # Some tracks don't have an artist and can't be scrobbled on Last.fm
    if not new_state.artist_name:
      self.stopped.emit()
      self.cannot_scrobble_error.emit('Music did not provide an artist name')
      return

    if new_state.is_playing:
      # Skip fetching track crop again if the song didn't change
      if self.__state:
        if (
          self.__state.track_title == new_state.track_title
          and self.__state.artist_name == new_state.artist_name
          and self.__state.album_title == new_state.album_title
          and self.__state.track_crop.finish # Check for track_finish so playing isn't emitted prematurely if track is play cycled repeatedly before AppleScript request can complete
        ):
          self.playing.emit(self.__state)
          return
    
    # Update cached state object with new state
    self.__state = new_state 

    # Fetch track crop data (start and finish timestamps)
    # Delay for 100ms to give enough time for AppleScript to update with new current track (Sometimes, AppleScript lags behind the notifications)
    timer = QtCore.QTimer(self)
    timer.setSingleShot(True) # Single-shot timer, basically setTimeout from JS
    timer.timeout.connect(self.__launch_fetch_track_crop_task)
    timer.start(100)

  def __launch_fetch_track_crop_task(self) -> None:
    get_library_track_crop = FetchTrackCrop(self.__applescript_app)
    get_library_track_crop.finished.connect(self.__handle_completion_of_get_track_crop_request)
    QtCore.QThreadPool.globalInstance().start(get_library_track_crop)
  
  def __handle_completion_of_get_track_crop_request(self, track_crop: TrackCrop) -> None:
    '''Figure out what to do with the results of the track crop request'''

    if track_crop.finish != 0:
      # A track finish was found, so we can use the actual crop values
      self.__state.track_crop = track_crop
    else:
      # No track finish was found (most likely a non-library track), we'll use the total duration as the track finish instead
      total_time = self.__cached_notification_payload.get('Total Time')

      if total_time:
        self.__state.track_crop.finish = total_time / 1000 # Convert from ms to s
      else:
        # Sometimes even this fails, there's nothing we can do
        self.stopped.emit()
        self.cannot_scrobble_error.emit('Music did not provide a track length')
        logger.error(f'Error getting track duration for {self.__cached_notification_payload}')

        # Don't emit play signal
        return
    
    # Finally emit play/pause signal
    if self.__state.is_playing:
      self.playing.emit(self.__state)
    else:
      self.paused.emit(self.__state)

  # Shows as unused because it has to be registered with pyobjc as a function name string
  def __handleNotificationFromMusic_(self, notification) -> None: # TODO: Add type annotation
    '''Handle Objective-C notifications for Music app events'''
    
    self.__cached_notification_payload = notification.userInfo()

    logger.trace(f'New notification from Music.app: {self.__cached_notification_payload}')

    if self.__cached_notification_payload['Player State'] == 'Stopped':
      self.stopped.emit()
      return

    self.__handle_new_state(
      MediaPlayerState(
        artist_name=self.__cached_notification_payload.get('Artist'),
        track_title=self.__cached_notification_payload.get('Name'),
        album_title=self.__cached_notification_payload.get('Album', None), # Prevent empty strings
        is_playing=self.__cached_notification_payload['Player State'] == 'Playing',
        position=self.get_player_position()
      )
    )