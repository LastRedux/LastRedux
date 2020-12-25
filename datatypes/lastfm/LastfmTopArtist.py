from dataclasses import dataclass

from datatypes.lastfm.LastfmArtist import LastfmArtist

@dataclass
class LastfmTopArtist(LastfmArtist):
  plays: int

  def __str__(self) -> str:
    return f'{super().__str__()} [{self.plays} plays]'