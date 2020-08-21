from ScriptingBridge import SBApplication

class AppleMusicPlugin():
  # From Music.app BridgeSupport enum definitions
  STOPPED_STATE = 1800426323
  PAUSED_STATE = 1800426352
  PLAYING_STATE = 1800426320
  
  def __init__(self):
    self.apple_music = SBApplication.applicationWithBundleIdentifier_('com.apple.Music')

  def has_track_loaded(self):
    '''Return whether there is a track loaded in the controls of the Music window'''
    
    return not self.apple_music.playerState() == self.STOPPED_STATE

  def get_current_track(self):
    track = self.apple_music.currentTrack()
    
    return {
      'title': track.name(),
      'artist_name': track.artist(),
      'album_name': track.album(),

      # Compensate for cropped tracks
      'start': track.start(),
      'finish': track.finish()
    }

  def get_player_position(self):
    return self.apple_music.playerPosition()