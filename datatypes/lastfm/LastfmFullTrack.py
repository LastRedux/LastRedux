from dataclasses import dataclass, field
from typing import List

from datatypes.lastfm.LastfmTopTrack import LastfmTopTrack
from datatypes.lastfm.LastfmTags import LastfmTags
from datatypes.lastfm.LastfmTag import LastfmTag

@dataclass
class LastfmFullTrack(LastfmTopTrack):
  is_loved: bool
  global_listeners: int
  global_plays: int
  tags: LastfmTags

  def __str__(self) -> str:
    return '\n'.join((
      super().__str__(),
      f'Loved: {self.is_loved}',
      f'Global Listeners: {self.global_listeners}',
      f'Global Plays: {self.global_plays}',
      f'Tags: {self.tags}'
    ))