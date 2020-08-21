from dataclasses import dataclass, field
from typing import List

from datatypes.Tag import Tag

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