from dataclasses import dataclass
from datetime import datetime

from datatypes.lastfm.LastfmTrack import LastfmTrack

@dataclass
class LastfmScrobble(LastfmTrack):
  timestamp: datetime