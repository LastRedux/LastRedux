from _future_ import annotations
from dataclasses import dataclass
from typing import List

from .LastfmList import LastfmList
from .LastfmTag import LastfmTag

@dataclass
class LastfmArtist:
  url: str
  name: str
  plays: int = None
  bio: str = None
  global_listeners: int = None
  global_plays: int = None
  tags: List[LastfmTag] = None
  similar_artists: LastfmList[LastfmArtist] = None

  def __repr__(self) -> str:
    string = self.name
    
    if self.plays:
      string += f' [{self.plays} plays]'

    return string

  def __eq__(self, o: LastfmArtist) -> bool:
    if not isinstance(o, LastfmArtist):
      return False

    return self.url == o.url