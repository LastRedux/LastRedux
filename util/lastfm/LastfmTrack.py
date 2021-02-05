from __future__ import annotations
from dataclasses import dataclass
from typing import List

from .LastfmArtistLink import LastfmArtistLink
from .LastfmTag import LastfmTag

@dataclass
class LastfmTrack:
  url: str
  title: str
  artist_link: LastfmArtistLink
  plays: int
  is_loved: bool
  global_listeners: int
  global_plays: int
  tags: List[LastfmTag]

  def __repr__(self) -> str:
    return f'{self.artist_link.name} - {self.title} [{self.plays} plays]'

  def __eq__(self, o: LastfmTrack) -> bool:
    if not isinstance(o, LastfmTrack):
      return False

    return self.url == o.url