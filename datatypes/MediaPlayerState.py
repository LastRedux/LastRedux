from dataclasses import dataclass

@dataclass
class MediaPlayerState:
  is_playing: bool
  track_title: str
  artist_name: str
  album_title: str
  track_end: float
  track_start: float = 0.0