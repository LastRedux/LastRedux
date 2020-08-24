from dataclasses import dataclass

@dataclass
class MediaPlayerState:
  has_track_loaded: bool = False
  player_position: str = None
  track_title: str = None
  artist_name: str = None
  album_title: str = None
  track_start: int = None
  track_finish: int = None
  error_message: str = ''