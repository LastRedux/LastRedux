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

  def __str__(self) -> str:
    return '\n'.join((
      f'{repr(self)} [{self.plays}]',
      f'User Plays: {self.plays}'
      f'Global Listeners: {self.global_listeners}',
      f'Global Plays: {self.global_plays}',
      f'Tags: {self.tags}'
    ))

  def __repr__(self) -> str:
    return f'{self.artist_link.name} - {self.title}'

  def __eq__(self, o: object) -> bool:
    return self.url == o.url