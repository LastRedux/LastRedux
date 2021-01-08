from __future__ import annotations
from dataclasses import dataclass, field
from typing import List

from datatypes.lastfm.LastfmList import LastfmList
from datatypes.lastfm.LastfmTag import LastfmTag

@dataclass
class LastfmArtistInfo:
  url: str
  name: str
  plays: int = None
  bio: str = None
  global_listeners: int = None
  global_plays: int = None
  tags: List[LastfmTag] = field(default_factory=list)
  similar_artists: LastfmList[LastfmArtistInfo] = field(default_factory=list)

  def __str__(self) -> str:
    return '\n'.join((
      f'{self.name} [{self.plays}]',
      f'Global Listeners: {self.global_listeners}',
      f'Global Plays: {self.global_plays}',
      f'Tags: {self.tags}',
      f'Similar Artists: {self.similar_artists}'
    ))

  def __repr__(self):
    return self.name