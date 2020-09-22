from ScriptingBridge import SBApplication

from plugins.MediaPlayerPlugin import MediaPlayerPlugin
from datatypes.MediaPlayerState import MediaPlayerState

class AppleMusicPlugin(MediaPlayerPlugin):
  # From Music.app BridgeSupport enum definitions
  STOPPED_STATE = 1800426323
  PAUSED_STATE = 1800426352
  PLAYING_STATE = 1800426320

  def __init__(self):
    self.apple_music = SBApplication.applicationWithBundleIdentifier_('com.apple.Music')

  def get_state(self) -> MediaPlayerState:
    # Store state in a new MediaPlayerState instance
    state = MediaPlayerState()

    # Only load track data when there is a track loaded in the controls of the Music window
    if self.apple_music.playerState() != self.STOPPED_STATE:
      current_track = self.apple_music.currentTrack()
      
      state.track_title = current_track.name()
      
      if state.track_title:
        state.artist_name = current_track.artist()
        
        if state.artist_name:
          state.player_position = self.apple_music.playerPosition()
          state.album_title = current_track.album()
          state.track_start = current_track.start()
          state.track_finish = current_track.finish()
          state.has_track_loaded = True
        else:
          # Manually added tracks need an artist to be scrobbled
          state.error_message = 'The currently playing track needs to be tagged with an artist to scrobble.'
      else:
        # Browse/search page error
        state.error_message = 'Due to a bug in Apple Music, Music.app can\'t provide track information. Try switching tracks.'

    return state