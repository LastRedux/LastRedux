from __future__ import annotations # For self-referential return type

from dataclasses import dataclass, field
from typing import List

from datatypes.Artist import Artist
from datatypes.Album import Album
from datatypes.SimilarArtist import SimilarArtist
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

  def load_lastfm_track_data(self, lastfm_track) -> None:
    self.lastfm_url = lastfm_track['url']
    self.lastfm_global_listeners = int(lastfm_track['listeners'])
    self.lastfm_global_plays = int(lastfm_track['playcount'])
    self.lastfm_plays = int(lastfm_track['userplaycount'])
    self.lastfm_is_loved = bool(int(lastfm_track['userloved'])) # Convert 0/1 to bool
    self.lastfm_tags = list(map(lambda tag: Tag(tag['name'], tag['url']), lastfm_track['toptags']['tag']))

  @staticmethod
  def build_from_lastfm_recent_track(lastfm_recent_track) -> Track:
    '''Build a Track from a user scrobble event (does NOT contain user plays nor global stats)'''

    artist = Artist(
      name=lastfm_recent_track['artist']['name'],
      lastfm_url=lastfm_recent_track['artist']['url'],
      image_url=''
    )

    album = Album(
      title=lastfm_recent_track['album']['#text'],
      image_url=lastfm_recent_track['image'][-1]['#text'], # Pick mega size in images array
      image_url_small=lastfm_recent_track['image'][1]['#text'] # Pick medium size in images array
    )

    return Track(
      title=lastfm_recent_track['name'],
      artist=artist,
      album=album,
      lastfm_url=lastfm_recent_track['url']
    )