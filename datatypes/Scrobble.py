from __future__ import annotations
from dataclasses import asdict, dataclass
from typing import List

from util.lastfm.LastfmScrobble import LastfmScrobble
from util.lastfm.LastfmTrack import LastfmTrack
from util.lastfm.LastfmAlbum import LastfmAlbum
from util.spotify_api import SpotifyArtist
from util.lastfm.LastfmArtist import LastfmArtist
from .MediaPlayerState import MediaPlayerState
from .ImageSet import ImageSet
from .ProfileStatistic import ProfileStatistic

@dataclass
class Scrobble(LastfmScrobble):
  image_set: ImageSet = None
  lastfm_track: LastfmTrack = None
  lastfm_artist: LastfmArtist = None
  lastfm_album: LastfmAlbum = None
  spotify_artists: List[SpotifyArtist] = None
  is_loading: bool = True
  lastfm_album_url: str = None # This is needed since the track info request doesn't give us an album
  friend_artist_leaderboard: List[ProfileStatistic] = None

  @staticmethod
  def from_lastfm_scrobble(lastfm_scrobble: LastfmScrobble) -> Scrobble:
    return Scrobble(**asdict(lastfm_scrobble))

  def is_equal_to_media_player_state(self, media_player_state: MediaPlayerState):
    return (
      self.track_title == media_player_state.track_title
      and self.artist_name == media_player_state.artist_name
      and self.album_title == media_player_state.album_title
    )