from dataclasses import dataclass

@dataclass
class Album:
  # Media player data
  title: str

  # iTunes store data
  image_url: str = ''
  image_url_small: str = ''

  # Last.fm data
  lastfm_url: str = ''