import logging

from ScriptingBridge import SBApplication
from Foundation import NSDistributedNotificationCenter

from datatypes.TrackCrop import TrackCrop
from plugins.macOS.MacMediaPlayerPlugin import MacMediaPlayerPlugin
from datatypes.MediaPlayerState import MediaPlayerState

class SpotifyPlugin(MacMediaPlayerPlugin):
  MEDIA_PLAYER_NAME = 'Spotify'
  MEDIA_PLAYER_ID = MEDIA_PLAYER_NAME
  IS_SUBMISSION_ENABLED = True

  def __init__(self) -> None:
    # Store reference to Spotify app in AppleScript
    self.__applescript_app = SBApplication.applicationWithBundleIdentifier_('com.spotify.client')

    super().__init__(self.__applescript_app)

    self.is_plugin_available = False

    # Store the current media player state
    self.__state: MediaPlayerState = None

    if self.__applescript_app:
      self.is_plugin_available = True

      # Set up NSNotificationCenter (refer to https://lethain.com/how-to-use-selectors-in-pyobjc)
      self.__default_center = NSDistributedNotificationCenter.defaultCenter()

      self.__default_center.addObserver_selector_name_object_(
        self,
        '__handleNotificationFromSpotify:',
        'com.spotify.client.PlaybackStateChanged',
        None
      )

  # --- Mac Media Player Implementation ---

  def request_initial_state(self) -> None:
    # Avoid making an AppleScript request if the app isn't running (if we do, the app will launch) or the app doesn't exist
    if not self.is_open():
      return

    is_playing = self.__applescript_app.playerState() == SpotifyPlugin.PLAYING_STATE

    if not is_playing:
      return

    track = self.__applescript_app.currentTrack()
    album_title = track.album() or None # Prevent storing empty strings in album_title key

    self.__handle_new_state(
      MediaPlayerState(
        is_playing=is_playing,
        position=self.get_player_position(),
        artist_name=track.artist(),
        track_title=track.name(),
        album_title=album_title,
        track_crop=TrackCrop(
          # Spotify tracks can't be cropped so we use duration
          finish=track.duration() / 1000 # Convert from ms to s
        )
      )
    )

  # --- Private Methods ---

  def __handleNotificationFromSpotify_(self, notification) -> None:
    '''Handle Objective-C notifications for Spotify events'''

    notification_payload = notification.userInfo()
    logging.debug(f'New notification from Spotify.app: {notification_payload}')

    if notification_payload['Player State'] == 'Stopped':
      self.stopped.emit()
      return
    elif notification_payload['Player State'] == 'Paused':
      self.paused.emit()
      return

    self.__handle_new_state(
      MediaPlayerState(
        artist_name=notification_payload.get('Artist'),
        track_title=notification_payload.get('Name'),
        album_title=notification_payload.get('Album', None), # Prevent empty strings
        is_playing=notification_payload['Player State'] == 'Playing',
        position=self.get_player_position(),
        track_crop=TrackCrop(
          # Spotify tracks can't be cropped so we use duration
          finish=notification_payload['Duration'] / 1000 # Convert from ms to s
        )
      )
    )
    
  def __handle_new_state(self, new_state: MediaPlayerState) -> None:
    # It's possible to add local files with no artist on Spotify that can't be scrobbled
    if not new_state.artist_name:
      self.stopped.emit()
      self.showNotification.emit('Track cannot be scrobbled', 'Spotify did not provide an artist name')
      return

    # Update cached state object with new state
    self.__state = new_state

    # Emit playing event if the track is more than 30 seconds long
    if (new_state.track_crop.finish - new_state.track_crop.start) > 30.0:
      self.playing.emit(self.__state)
    else:
      self.showNotification.emit('Track cannot be scobbled', 'Track length is less than 30 seconds')