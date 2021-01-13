from __future__ import annotations
from dataclasses import asdict, dataclass

from datatypes.ImageSet import ImageSet
from util.lastfm.LastfmScrobble import LastfmScrobble
from util.lastfm.LastfmTrackInfo import LastfmTrack

@dataclass
class Scrobble(LastfmScrobble):
  image_set: ImageSet = None
  lastfm_track: LastfmTrack = None

  @staticmethod
  def from_lastfm_scrobble(lastfm_scrobble: LastfmScrobble) -> Scrobble:
    return Scrobble(**asdict(lastfm_scrobble))

  def is_equal_to_media_player_state(self, media_player_state: MediaPlayerState):
    return (
      self.track_title == media_player_state.track_title
      and self.artist_name == media_player_state.artist_name
      and self.album_title == media_player_state.album_title
    )