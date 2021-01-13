from PySide2 import QtCore
from ScriptingBridge import SBApplication
from Foundation import NSDistributedNotificationCenter
from loguru import logger

from plugins.macOS.MacMediaPlayerPlugin import MacMediaPlayerPlugin
from datatypes import MediaPlayerState, TrackCrop
from .FetchTrackCrop import FetchTrackCrop

class MusicAppPlugin(MacMediaPlayerPlugin): # QObject not needed since all MediaPlayers inherit from it
  does_not_have_artist_error = QtCore.Signal()

  def __init__(self):
    super().__init__()

    # Store reference to Music app in AppleScript
    self.__applescript_app = SBApplication.applicationWithBundleIdentifier_('com.apple.Music')

    # Set up NSNotificationCenter (refer to https://lethain.com/how-to-use-selectors-in-pyobjc)
    self.__default_center = NSDistributedNotificationCenter.defaultCenter()
    self.__default_center.addObserver_selector_name_object_(self, '__handleNotificationFromMusic:', 'com.apple.Music.playerInfo', None)

    # Store the latest notification from NSNotificationObserver
    self.__cached_notification_payload: dict = None

    # Store latest state
    self.__state: MediaPlayerState = None

  def __str__(self):
    return 'Music'

  # --- Media Player Implementation ---

  def request_initial_state(self):
    # Avoid making an AppleScript request if the app isn't running (if we do, the app will launch)
    if (
      not self.__applescript_app.isRunning()
      or self.__applescript_app.playerState() != MusicAppPlugin.PLAYING_STATE
    ):
      return

    track = self.__applescript_app.currentTrack()
    track_title = track.name()
    
    if not track_title:
      # User is playing a non-library track, so AppleScript can't see the data
      # Instead, we have to force a play notification
      self.__applescript_app.pause()
      self.__applescript_app.playpause() # There is no play function for whatever reason
      return

    self.__state = MediaPlayerState(
      is_playing=True,
      artist_name=track.artist(),
      track_title=track_title,
      album_title=track.album() or None, # Prevent storing empty strings in album_title key
      track_crop=TrackCrop(
        finish=track.duration() # In seconds
        # No start value since Apple Music doesn't allow non-library tracks to be cropped
      )
    )

    # Wait 1 second for the HistoryViewModel to load before sending initial playing signal
    timer = QtCore.QTimer(self)
    timer.setSingleShot(True) # Single-shot timer, basically setTimeout from JS
    timer.timeout.connect(lambda: self.playing.emit(self.__state))
    timer.start(1000)

  # --- Private Methods ---

  # Shows as unused because it has to be registered with pyobjc as a function name string
  def __handleNotificationFromMusic_(self, notification): # TODO: Add type annotation
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
    
    album_title = self.__cached_notification_payload['Album'] or None # Prevent storing empty strings in album_title key
    
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

      if not total_time:
        # Sometimes even this fails, there's nothing we can do
        # TODO: Alert the user to the fact that their track can't be scrobbled
        logger.error(f'Error getting track duration for {self.__cached_notification_payload}')

      self.__state.track_crop.finish = total_time / 1000 # Convert from ms to s
    
    # Finally emit play/pause signal
    if self.__state.is_playing:
      self.playing.emit(self.__state)
    else:
      self.paused.emit(self.__state)