from __future__ import annotations
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

  def __repr__(self):
    return self.name + (f' [{self.plays} plays]' if self.plays else '')

  def __eq__(self, o: object) -> bool:
    return self.url == o.url