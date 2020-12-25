from dataclasses import dataclass
from typing import List

from datatypes.lastfm.LastfmTopAlbum import LastfmTopAlbum

@dataclass
class LastfmTopAlbums:
  albums: List[LastfmTopAlbum]
  total: int

  def __str__(self) -> str:
    return '\n'.join([album.__str__() for album in self.albums])