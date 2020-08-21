from dataclasses import dataclass

@dataclass
class SimilarArtist:
  name: str
  lastfm_url: str
  image_url: str = ''