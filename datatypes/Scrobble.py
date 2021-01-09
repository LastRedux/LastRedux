from dataclasses import dataclass
from datetime import datetime

from datatypes.SimpleTrack import SimpleTrack
from datatypes.ImageSet import ImageSet
from util.lastfm.LastfmTrackInfo import LastfmTrackInfo
from datatypes.MediaPlayerState import MediaPlayerState

@dataclass
class Scrobble(SimpleTrack):
  timestamp: datetime
  image_set: ImageSet
  lastfm_track: LastfmTrackInfo = None
  
  @classmethod
  def from_media_player_state(cls, state: MediaPlayerState):
    return cls(datetime.now(), state.track_title, state.artist_name, state.album_title)