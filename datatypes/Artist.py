from __future__ import annotations # For self-referential return type
from dataclasses import dataclass, field

from typing import List

from datatypes.Tag import Tag
from datatypes.SimilarArtist import SimilarArtist

@dataclass
class Artist:
  # Media player data
  name: str

  # iTunes store data
  image_url: str = ''

  # Last.fm data
  # TODO: Use create Artist.lastfm_data with empty default
  lastfm_url: str = ''
  lastfm_global_listeners: int = 0
  lastfm_global_plays: int = 0
  lastfm_plays: int = 0
  lastfm_bio: str = ''
  lastfm_tags: List[Tag] = field(default_factory=list)
  lastfm_similar_artists: List[SimilarArtist] = field(default_factory=list)

  @staticmethod
  def build_from_lastfm_artist(lastfm_artist) -> Artist:
    return Artist(
      name=lastfm_artist['name'],
      image_url='',
      lastfm_url=lastfm_artist['url'],
      lastfm_plays=lastfm_artist['playcount'],
    )