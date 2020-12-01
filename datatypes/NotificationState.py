from dataclasses import dataclass

@dataclass
class NotificationState:
  track_title: str = None
  artist_name: str = None
  track_duration: float = None
  album_title: str = None # Not every track has an album