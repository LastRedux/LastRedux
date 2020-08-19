from dataclasses import dataclass

@dataclass
class Album:
  title: str
  image_url: str = ''
  image_url_small: str = ''
  lastfm_plays: int = 0
  lastfm_url: str = ''