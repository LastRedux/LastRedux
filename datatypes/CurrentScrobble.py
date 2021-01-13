from dataclasses import dataclass

@dataclass
class CurrentScrobble:
  track_title: str
  artist_name: str
  image_url: str
  is_loved: bool
  scrobble_percentage: float