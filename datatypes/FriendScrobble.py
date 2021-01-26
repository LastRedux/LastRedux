from __future__ import annotations
from dataclasses import dataclass

from .SimpleTrack import SimpleTrack

@dataclass
class FriendScrobble(SimpleTrack):
  url: str
  artist_url: str
  image_url: str
  is_playing: bool
  is_loved: bool

  def __eq__(self, o: FriendScrobble) -> bool:
    return (
      self.url == o.url
      and self.is_loved == o.is_loved
      and self.is_playing == o.is_playing
    )

  def __repr__(self):
      return super().__repr__()