from dataclasses import dataclass

from .SimpleTrack import SimpleTrack

@dataclass
class FriendScrobble(SimpleTrack):
  url: str
  artist_url: str
  image_url: str
  is_playing: bool
  is_loved: bool