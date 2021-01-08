from dataclasses import dataclass, field
from typing import List

from datatypes.lastfm.LastfmArtistInfo import LastfmArtistInfo
from datatypes.lastfm.LastfmAlbumInfo import LastfmAlbumInfo
from datatypes.lastfm.LastfmTag import LastfmTag

@dataclass
class LastfmTrackInfo:
  url: str
  title: str
  artist: LastfmArtistInfo
  album: LastfmAlbumInfo = None
  plays: int = None
  is_loved: bool = None
  global_listeners: int = None
  global_plays: int = None
  tags: List[LastfmTag] = field(default_factory=list)

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