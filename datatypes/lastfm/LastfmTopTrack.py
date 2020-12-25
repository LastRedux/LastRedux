from dataclasses import dataclass

from datatypes.lastfm.LastfmHistoryTrack import LastfmHistoryTrack

@dataclass
class LastfmTopTrack(LastfmHistoryTrack):
  plays: int

  def __str__(self) -> str:
    return f'{super().__str__()} [{self.plays} plays]'