from __future__ import annotations # For self-referential return type

from dataclasses import dataclass, field
from typing import List

from datatypes.Artist import Artist
from datatypes.Album import Album
from datatypes.Tag import Tag

@dataclass
class Track:
  # Media player data
  title: str
  artist: Artist
  album: Album

  # Last.fm data
  lastfm_url: str = ''
  lastfm_global_listeners: int = 0
  lastfm_global_plays: int = 0
  lastfm_plays: int = 0
  lastfm_is_loved: bool = False
  lastfm_tags: List[Tag] = field(default_factory=list)

  # Loading state
  # TODO: Move to Scrobble eventually
  has_requested_lastfm_data: bool = False
  has_lastfm_data: bool = False
  has_itunes_store_data: bool = False

  @staticmethod
  def build_from_lastfm_track(lastfm_track) -> Track:
    artist = Artist(
      name=lastfm_track['artist']['name'],
      image_url=''
    )

    album = Album(
      title=lastfm_track['album']['#text'],
      image_url=lastfm_track['image'][-1]['#text'], # Pick mega size in images array
      image_url_small=lastfm_track['image'][1]['#text'] # Pick medium size in images array
    )

    return Track(
      title=lastfm_track['name'],
      artist=artist,
      album=album
    )