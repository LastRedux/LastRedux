from dataclasses import dataclass
from typing import List

from datatypes.lastfm.LastfmArtist import LastfmArtist

@dataclass
class LastfmArtists:
  artists: List[LastfmArtist]

  def __str__(self) -> str:
    return f'[{", ".join([artist.__str__() for artist in self.artists])}]'