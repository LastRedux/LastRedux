from dataclasses import dataclass
from datetime import datetime

from datatypes.SimpleTrack import SimpleTrack

@dataclass
class LastfmScrobble(SimpleTrack):
  timestamp: datetime

  def __repr__(self) -> str:
    string = super()._repr_()
    
    if self.timestamp:
      string += f' {self.timestamp.strftime("%Y-%m-%d %H:%M:%S")}'
    else:
      string += ' (Now Playing)'

    return string