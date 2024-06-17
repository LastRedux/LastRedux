from dataclasses import dataclass, field

from .SimpleTrack import SimpleTrack
from .TrackCrop import TrackCrop


@dataclass
class MediaPlayerState(SimpleTrack):
    is_playing: bool
    position: float
    track_crop: TrackCrop = field(default_factory=TrackCrop)
