from dataclasses import dataclass, field
from typing import List

from datatypes.lastfm.LastfmTopAlbum import LastfmTopAlbum
from datatypes.lastfm.LastfmTags import LastfmTags

@dataclass
class LastfmFullAlbum(LastfmTopAlbum):
  global_listeners: int
  global_plays: int
  tags: LastfmTags

  def __str__(self) -> str:
    return '\n'.join((
      super().__str__(),
      f'Global Listeners: {self.global_listeners}',
      f'Global Plays: {self.global_plays}',
      f'Tags: {self.tags}',
    ))