from dataclasses import dataclass
from typing import List

from .LastfmAlbum import LastfmAlbum
from .LastfmArtist import LastfmArtist
from .LastfmTag import LastfmTag

@dataclass
class LastfmTrack:
  url: str
  title: str
  artist: LastfmArtist
  album: LastfmAlbum = None
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
    string =  f'{self.artist.name} - {self.title}'
    
    if self.album:
      string += f' | {self.album.title}'

    return string