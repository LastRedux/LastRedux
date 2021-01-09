# from typing import Dict

from PySide2 import QtCore
from ScriptingBridge import SBApplication
from Foundation import NSDistributedNotificationCenter
# from loguru import logger

from datatypes.MediaPlayerState import MediaPlayerState

class SpotifyPlugin(QtCore.QObject):
  # Integer AppleScript states from ScriptingBridge
  STOPPED_STATE = 1800426323
  PAUSED_STATE = 1800426352
  PLAYING_STATE = 1800426320

  # Media player signals
  stopped = QtCore.Signal()
  paused = QtCore.Signal(MediaPlayerState)
  playing = QtCore.Signal(MediaPlayerState)

  def __init__(self):
    QtCore.QObject.__init__(self)

    # Store the current media player state
    self.__state: MediaPlayerState = None

    # Store reference to Spotify app in AppleScript
    self.__applescript_spotify_app = SBApplication.applicationWithBundleIdentifier_('com.spotify.client')

    # Set up NSNotificationCenter (refer to https://lethain.com/how-to-use-selectors-in-pyobjc)
    self.__default_center = NSDistributedNotificationCenter.defaultCenter()
    self.__default_center.addObserver_selector_name_object_(self, '__handleNotificationFromSpotify:', 'com.spotify.client.PlaybackStateChanged', None)

    # Get current song on launch without waiting for a playing notification (the user is already listening to something)
    if self.is_open():
      # Only load if something is already playing
      if self.__applescript_spotify_app.playerState() == SpotifyPlugin.PLAYING_STATE:
        self.request_initial_state()

  def __str__(self):
    return 'Spotify'

  # --- Media Player Implementation ---

  def get_player_position(self) -> float:
    return self.__applescript_spotify_app.playerPosition()

  def is_open(self):
    return self.__applescript_spotify_app.isRunning()

  def request_initial_state(self):
    # Avoid making an AppleScript request if the app isn't running (if we do, the app will launch)
    if not self.__applescript_spotify_app.isRunning():
      return

    track = self.__applescript_spotify_app.currentTrack()
    album_title = track.album() or None # Prevent storing empty strings in album_title key

    self.__state = MediaPlayerState(
      is_playing=self.__applescript_spotify_app.playerState() == SpotifyPlugin.PLAYING_STATE,
      artist_name=track.artist(),
      track_title=track.name(),
      album_title=album_title,
      track_start=0,
      track_finish=track.duration() / 1000 # Convert from ms to s
    )
    
    # Wait 1 second for the HistoryViewModel to load before sending initial playing signal
    timer = QtCore.QTimer(self)
    timer.setSingleShot(True) # Single-shot timer, basically setTimeout from JS
    timer.timeout.connect(lambda: self.playing.emit(self.__state) if self.__state.is_playing else self.paused.emit(self.__state))
    timer.start(1000)

  # --- Private Methods ---

  def __handleNotificationFromSpotify_(self, notification):
    '''Handle Objective-C notifications for Spotify events'''

    notification_payload = notification.userInfo()
    player_state = notification_payload['Player State']

    if player_state == 'Stopped':
      self.stopped.emit()
      return

    track_title = notification_payload['Name'] # This should never be blank on Spotify
    artist_name = notification_payload.get('Artist')

    # Some tracks don't have an artist and can't be scrobbled on Last.fm
    if not artist_name:
      self.stopped.emit()
      return

    is_playing = player_state == 'Playing'

    # Detect if paused to emit paused signal without running AppleScript again
    # Make sure that we have track data first
    if self.__state and not is_playing:
      self.paused.emit(self.__state)
      return
    
    album_title = notification_payload['Album'] or None # Prevent storing empty strings in album_title key
    
    # Emit play signal early and skip AppleScript if the track is the same as the last one (if it exists)
    if self.__state:
      if self.__state.track_title == track_title and self.__state.artist_name == artist_name and self.__state.album_title == album_title and self.__state.track_finish: # Check for track_finish so playing isn't emitted prematurely if track is play cycled repeatedly before AppleScript request can complete
        self.playing.emit(self.__state)
        return
    
    # Create new state object to store new track data
    self.__state = MediaPlayerState(
      is_playing, 
      track_title, 
      artist_name, 
      album_title, 
      track_start=0, 
      track_finish=notification_payload['Duration'] / 1000 # Convert from ms to s
    )
    self.playing.emit(self.__state)