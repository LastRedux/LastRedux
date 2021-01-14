from __future__ import annotations
from dataclasses import asdict, dataclass
from typing import List

from datatypes import MediaPlayerState, ImageSet
from util.lastfm import LastfmScrobble, LastfmTrack
from util.spotify_api import SpotifyArtist

@dataclass
class Scrobble(LastfmScrobble):
  image_set: ImageSet = None
  lastfm_track: LastfmTrack = None
  spotify_artists: List[SpotifyArtist] = None
  is_loading: bool = True
  lastfm_album_url: str = None # This is needed since the track info request doesn't give us an album

  @staticmethod
  def from_lastfm_scrobble(lastfm_scrobble: LastfmScrobble) -> Scrobble:
    return Scrobble(**asdict(lastfm_scrobble))

  def is_equal_to_media_player_state(self, media_player_state: MediaPlayerState):
    return (
      self.track_title == media_player_state.track_title
      and self.artist_name == media_player_state.artist_name
      and self.album_title == media_player_state.album_title
    )