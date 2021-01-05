from dataclasses import dataclass
from typing import List

from datatypes.lastfm.LastfmScrobble import LastfmScrobble

@dataclass
class LastfmScrobbles:
  tracks: List[LastfmScrobble]
  total: int

  def __str__(self) -> str:
    return '\n'.join([track.__str__() for track in self.tracks])