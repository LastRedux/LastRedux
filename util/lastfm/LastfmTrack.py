from _future_ import annotations
from dataclasses import dataclass
from typing import List

from .LastfmArtistLink import LastfmArtistLink
from .LastfmTag import LastfmTag

@dataclass
class LastfmTrack:
  url: str
  title: str
  artist_link: LastfmArtistLink

  # Optional data
  plays: int = None
  is_loved: bool = None
  global_listeners: int = None
  global_plays: int = None
  tags: List[LastfmTag] = None

  def __repr__(self) -> str:
    return f'{self.artist_link.name} - {self.title}'

  def __eq__(self, o: LastfmTrack) -> bool:
    if not isinstance(o, LastfmTrack):
      return False

    return self.url == o.url