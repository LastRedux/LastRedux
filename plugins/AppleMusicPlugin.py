from ScriptingBridge import SBApplication

from datatypes.MediaPlayerState import MediaPlayerState

class AppleMusicPlugin():
  # From Music.app BridgeSupport enum definitions
  STOPPED_STATE = 1800426323
  PAUSED_STATE = 1800426352
  PLAYING_STATE = 1800426320

  def __init__(self):
    self.apple_music = SBApplication.applicationWithBundleIdentifier_('com.apple.Music')

  def get_state(self):
    '''Get Apple Music player state and current track if it is running'''

    # Store state in a new MediaPlayerState instance
    state = MediaPlayerState()

    # Only load track data when there is a track loaded in the controls of the Music window
    if self.apple_music.playerState() != self.STOPPED_STATE:
      current_track = self.apple_music.currentTrack()
      
      state.player_position = self.apple_music.playerPosition()
      state.has_track_loaded = True
      state.track_title = current_track.name()
      state.album_title = current_track.album()
      state.artist_name = current_track.artist()
      state.track_start = current_track.start()
      state.track_finish = current_track.finish()

      if not state.track_title or not state.album_title or not state.artist_name:
        state.error_message = 'Due to a bug in Apple Music, Music.app failed to provide track information for the current track. Try switching tracks and then switching back.'

    return state