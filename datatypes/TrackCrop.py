from dataclasses import dataclass


@dataclass
class TrackCrop:
    # Both in seconds
    start: float = 0.0
    finish: float = None
