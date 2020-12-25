from dataclasses import dataclass
from typing import List

from datatypes.lastfm.LastfmTopArtist import LastfmTopArtist

@dataclass
class LastfmTopArtists:
  artists: List[LastfmTopArtist]
  total: int

  def __str__(self) -> str:
    return '\n'.join([artist.__str__() for artist in self.artists])