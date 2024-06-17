from dataclasses import dataclass
from typing import List

from util.spotify_api.SpotifyArtist import SpotifyArtist
from datatypes.ImageSet import ImageSet


@dataclass
class ScrobbleImages:
    album_art: ImageSet
    spotify_artists: List[SpotifyArtist]
