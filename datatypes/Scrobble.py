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