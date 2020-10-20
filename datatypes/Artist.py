from __future__ import annotations # For self-referential return type
from dataclasses import dataclass, field

from typing import List

from datatypes.Tag import Tag
from datatypes.SimilarArtist import SimilarArtist

@dataclass
class Artist:
  name: str
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

  def load_lastfm_artist_data(self, lastfm_artist) -> None:
    self.lastfm_url = lastfm_artist['url']
    self.lastfm_global_listeners = int(lastfm_artist['stats']['listeners'])
    self.lastfm_global_plays = int(lastfm_artist['stats']['playcount'])
    self.lastfm_plays = int(lastfm_artist['stats']['userplaycount'])
    self.lastfm_bio = lastfm_artist['bio']['content'].split(' <')[0].strip() # Remove read more on Last.fm link because a QML Link component is used instead
    self.lastfm_tags = list(map(lambda tag: Tag(tag['name'], tag['url']), lastfm_artist['tags']['tag']))
    self.lastfm_similar_artists = list(map(lambda similar_artist: SimilarArtist(similar_artist['name'], similar_artist['url']), lastfm_artist['similar']['artist']))
