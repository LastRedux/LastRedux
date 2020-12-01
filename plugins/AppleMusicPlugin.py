from PySide2 import QtCore
from ScriptingBridge import SBApplication
from Foundation import NSDistributedNotificationCenter

from datatypes.NotificationState import NotificationState
from datatypes.AppleScriptState import AppleScriptState

class AppleMusicPlugin(QtCore.QObject):
  stopped = QtCore.Signal()
  does_not_have_artist_error = QtCore.Signal()

  # From Music.app BridgeSupport enum definitions
  STOPPED_STATE = 1800426323
  PAUSED_STATE = 1800426352
  PLAYING_STATE = 1800426320

  def __init__(self):
    QtCore.QObject.__init__(self)

    # Set up AppleScript
    self.apple_music = SBApplication.applicationWithBundleIdentifier_('com.apple.Music')

    # Set up NSNotificationCenter
    # Using https://lethain.com/how-to-use-selectors-in-pyobjc/ as reference
    self.default_center = NSDistributedNotificationCenter.defaultCenter()
    observer = self.default_center.addObserver_selector_name_object_(self, 'handleNotificationFromMusic:', 'com.apple.iTunes.playerInfo', None) # TODO: Don't save to variable?
  
  # Objective-C function handling play/pause events
  def handleNotificationFromMusic_(self, notification):
    notification_payload = notification.userInfo()
    player_state = notification_payload['Player State']

    if player_state == 'Stopped':
      self.stopped.emit()
      return
    
    track_title = notification_payload['Name']

    # Apple Music puts Connecting... state string in the track title field for some reason
    if track_title == 'Connecting…':
      # Connecting... state should remove track from details pane and deselect it, so we're pretending the player is stopped
      self.stopped.emit()
      return

    artist_name = notification_payload.get('Artist')

    # Some tracks don't have an artist and can't be scrobbled on Last.fm
    if not artist_name:
      self.does_not_have_artist_error.emit()
      return
    
    album_title = notification_payload['Album']
    track_duration = notification_payload['Duration']
    notification_state = NotificationState(track_title, artist_name, track_duration, album_title)
    
    if player_state == 'Playing':
      self.playing.emit(notification_state)
    else:
      self.paused.emit(notification_state)
    
    timer = QtCore.QTimer(self)
    timer.timeout.connect(self.__handle_getting_the_length_after_the_timer)
    timer.setSingleShot(True)
    timer.start(100)
  
  def __handle_getting_the_length_after_the_timer(self):
    print('working')
  
  def get_local_track_length(self) -> AppleScriptState:
    state = AppleScriptState()

    if self.apple_music.playerState() != self.STOPPED_STATE:
      current_track = self.apple_music.currentTrack()
      state.track_start = current_track.start()
      state.track_finish = current_track.finish()
    
    return state

  def get_player_position(self) -> float:
    return self.apple_music.playerPosition()