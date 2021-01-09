from dataclasses import dataclass
from typing import List

from .SpotifyArtist import SpotifyArtist
from datatypes.ImageSet import ImageSet

@dataclass
class SpotifyImages:
  artists: List[SpotifyArtist]
  album_art: ImageSet