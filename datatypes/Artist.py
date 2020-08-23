from dataclasses import dataclass, field
from typing import List

from datatypes.Tag import Tag
from datatypes.SimilarArtist import SimilarArtist

@dataclass
class Artist:
  name: str
  image_url: str = ''
  lastfm_url: str = ''
  lastfm_bio: str = ''
  lastfm_global_listeners: int = 0
  lastfm_global_plays: int = 0
  lastfm_plays: int = 0
  lastfm_tags: List[Tag] = field(default_factory=list)
  lastfm_similar_artists: List[SimilarArtist] = field(default_factory=list)