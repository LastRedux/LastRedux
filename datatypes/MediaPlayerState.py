from dataclasses import dataclass

@dataclass
class MediaPlayerState(Track):
  is_playing: bool

  # Track crop data (in seconds)
  track_start: float = 0.0
  track_finish: float = None