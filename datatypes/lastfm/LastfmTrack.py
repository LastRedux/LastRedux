from dataclasses import dataclass

@dataclass
class LastfmTrack:
  url: str
  title: str
  track_image_url: str
  track_image_url_small: str
  artist_name: str
  artist_url: str
  album_title: str
  album_url: str

  def __str__(self) -> str:
    return f'{self.artist_name} - {self.title}'