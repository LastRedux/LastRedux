from typing import Dict

from PySide2 import QtCore
from ScriptingBridge import SBApplication
from Foundation import NSDistributedNotificationCenter
from loguru import logger

from datatypes.MediaPlayerState import MediaPlayerState
from tasks.FetchAppleMusicTrackCrop import FetchAppleMusicTrackCrop

class AppleMusicPlugin(QtCore.QObject):
  # From Music.app BridgeSupport enum definitions
  PLAYING_STATE = 1800426320

  stopped = QtCore.Signal()
  paused = QtCore.Signal(MediaPlayerState)
  playing = QtCore.Signal(MediaPlayerState)
  does_not_have_artist_error = QtCore.Signal()

  def __init__(self):
    QtCore.QObject.__init__(self)

    # Set up AppleScript
    self.apple_music = SBApplication.applicationWithBundleIdentifier_('com.apple.Music')

    # Set up NSNotificationCenter
    # Using https://lethain.com/how-to-use-selectors-in-pyobjc/ as reference
    self.default_center = NSDistributedNotificationCenter.defaultCenter()
    self.default_center.addObserver_selector_name_object_(self, 'handleNotificationFromMusic:', 'com.apple.iTunes.playerInfo', None)
    
    # Store the latest media player state received by the observer
    self.current_state = None

    # Store the latest notification from NSNotificationObserver to access it from multiple methods
    self.notification_payload = None

    # Pause-play to get a new play notification with player data if something is already playing
    if self.apple_music.isRunning():
      # Only pause-play if something is already playing
      if self.apple_music.playerState() == AppleMusicPlugin.PLAYING_STATE:
        self.apple_music.pause()
        self.apple_music.playpause()
    
  # Objective-C function handling play/pause events
  def handleNotificationFromMusic_(self, notification):
    self.notification_payload = notification.userInfo()
    player_state = self.notification_payload['Player State']

    if player_state == 'Stopped':
      self.stopped.emit()
      return
    
    track_title = self.notification_payload.get('Name')

    # Ignore notification if there's no track title (Usually happens with radio stations)
    if not track_title:
      return

    # Apple Music puts Connecting... state string in the track title field for some reason
    if track_title == 'Connecting…': # TODO: Find way to check this that works with other languages
      # Connecting... state should remove track from details pane and deselect it, so we're pretending the player is stopped
      self.stopped.emit()
      return

    artist_name = self.notification_payload.get('Artist')

    # Some tracks don't have an artist and can't be scrobbled on Last.fm
    if not artist_name:
      self.does_not_have_artist_error.emit()
      self.stopped.emit()
      return

    is_playing = player_state == 'Playing'

    # Detect if paused to emit paused signal without running AppleScript again
    # Make sure that we have track data first
    if self.current_state and not is_playing:
      self.paused.emit(self.current_state)
      return
    
    album_title = self.notification_payload.get('Album', '')
    
    # Emit play signal early and skip AppleScript if the track is the same as the last one (if it exists)
    if self.current_state:
      if self.current_state.track_title == track_title and self.current_state.artist_name == artist_name and self.current_state.album_title == album_title and self.current_state.track_finish: # Check for track_finish so playing isn't emitted prematurely if track is play cycled repeatedly before AppleScript request can complete
        self.playing.emit(self.current_state)
        return
    
    # Create new state object to store new track data
    self.current_state = MediaPlayerState(is_playing, track_title, artist_name, album_title)
    
    # Fetch track crop data (start and finish timestamps)
    # Delay for 100ms to give enough time for AppleScript to update with new current track (Sometimes, AppleScript lags behind the notifications)
    timer = QtCore.QTimer(self)
    timer.timeout.connect(self.__handle_getting_track_crop_after_the_timer)
    timer.setSingleShot(True) # Single-shot timer, basically setTimeout from JS
    timer.start(500)
  
  def __handle_getting_track_crop_after_the_timer(self):
    get_library_track_crop = FetchAppleMusicTrackCrop(self)
    get_library_track_crop.finished.connect(self.__handle_completion_of_get_track_crop_request)
    QtCore.QThreadPool.globalInstance().start(get_library_track_crop)
  
  def __handle_completion_of_get_track_crop_request(self, track_crop):
    # Use AppleScript start and finish values if they were found, otherwise leave the end value as is
    if track_crop['track_finish'] != 0:
      self.current_state.track_start = track_crop['track_start'] 
      self.current_state.track_finish = track_crop['track_finish']
    else:
      total_time = self.notification_payload.get('Total Time')

      if total_time:
        self.current_state.track_finish = total_time / 1000 # Convert from ms to s
      else:
        logger.error(f'Error getting track duration for {self.notification_payload.get("Name")}')
    
    # Finally emit play/pause signal
    if self.current_state.is_playing:
      self.playing.emit(self.current_state)
    else:
      self.paused.emit(self.current_state)
  
  def get_library_track_crop(self) -> Dict[float, float]:
    '''Use AppleScript to fetch the current track's start and finish timestamps (This often fails and returns 0.0 for both)'''

    current_track = self.apple_music.currentTrack()

    return {
      'track_start': current_track.start(),
      'track_finish': current_track.finish()
    }

  def get_player_position(self) -> float:
    '''Use AppleScript to fetch the current Apple Music playback position'''

    return self.apple_music.playerPosition()