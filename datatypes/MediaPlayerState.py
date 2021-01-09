from dataclasses import dataclass

from datatypes.SimpleTrack import SimpleTrack

@dataclass
class MediaPlayerState(SimpleTrack):
  is_playing: bool

  # Track crop data (in seconds)
  track_start: float = 0.0
  track_finish: float = None