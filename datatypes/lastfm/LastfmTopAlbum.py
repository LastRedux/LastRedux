from dataclasses import dataclass

from datatypes.lastfm.LastfmAlbum import LastfmAlbum

@dataclass
class LastfmTopAlbum(LastfmAlbum):
  plays: int

  def __str__(self) -> str:
    return f'{super().__str__()} [{self.plays} plays]'