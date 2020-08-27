from dataclasses import dataclass, field
from typing import List

from datatypes.Artist import Artist
from datatypes.Album import Album
from datatypes.Tag import Tag

@dataclass
class Track:
  title: str
  artist: Artist
  album: Album
  has_lastfm_data: bool = False # TODO: Move has_lastfm_data and has_itunes_store_data to Scrobble
  has_itunes_store_data: bool = False
  lastfm_url: str = ''
  lastfm_is_loved: bool = False
  lastfm_plays: int = 0
  lastfm_tags: List[Tag] = field(default_factory=list)