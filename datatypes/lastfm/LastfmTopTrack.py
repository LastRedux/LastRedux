from dataclasses import dataclass

from datatypes.lastfm.LastfmTrack import LastfmTrack

@dataclass
class LastfmTopTrack(LastfmTrack):
  plays: int

  def __str__(self) -> str:
    return f'{super().__str__()} [{self.plays} plays]'