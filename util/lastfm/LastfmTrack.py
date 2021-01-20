from dataclasses import dataclass
from typing import List

from .LastfmArtistReference import LastfmArtistReference
from .LastfmAlbum import LastfmAlbum
from .LastfmTag import LastfmTag

@dataclass
class LastfmTrack:
  url: str
  title: str
  artist_reference: LastfmArtistReference

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
    return f'{self.artist_reference.name} - {self.title}'