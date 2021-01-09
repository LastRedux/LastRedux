from dataclasses import dataclass, field
from typing import List

from .LastfmArtistInfo import LastfmArtistInfo
from .LastfmTag import LastfmTag
from datatypes import ImageSet

@dataclass
class LastfmAlbumInfo:
  url: str
  title: str
  artist: LastfmArtistInfo
  image_set: ImageSet
  plays: int

  # TODO: Actually display this data
  global_listeners: int = None
  global_plays: int = None
  tags: List[LastfmTag] = field(default_factory=list)

  def __str__(self) -> str:
    return '\n'.join((
      f'{repr(self)} [{self.plays}]',
      f'Global Listeners: {self.global_listeners}',
      f'Global Plays: {self.global_plays}',
      f'Tags: {self.tags}'
    ))

  def __repr__(self) -> str:
    return f'{self.title} | {self.artist.name}'