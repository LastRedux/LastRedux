from dataclasses import dataclass, field
from typing import List

from datatypes.lastfm.LastfmTopArtist import LastfmTopArtist
from datatypes.lastfm.LastfmArtists import LastfmArtists
from datatypes.lastfm.LastfmTags import LastfmTags

@dataclass
class LastfmFullArtist(LastfmTopArtist):
  global_listeners: int
  global_plays: int
  bio: str
  tags: LastfmTags
  similar_artists: LastfmArtists

  def __str__(self) -> str:
    return '\n'.join((
      super().__str__(),
      f'Global Listeners: {self.global_listeners}',
      f'Global Plays: {self.global_plays}',
      f'Tags: {self.tags}',
      f'Similar Artists: {self.similar_artists}'
    ))