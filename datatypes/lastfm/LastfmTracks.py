from dataclasses import dataclass
from typing import List

from datatypes.lastfm.LastfmHistoryTrack import LastfmHistoryTrack

@dataclass
class LastfmTracks:
  tracks: List[LastfmHistoryTrack]
  total: int

  def __str__(self) -> str:
    return '\n'.join([track.__str__() for track in self.tracks])