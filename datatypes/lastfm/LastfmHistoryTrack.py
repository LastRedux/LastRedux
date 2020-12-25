from dataclasses import dataclass

@dataclass
class LastfmHistoryTrack:
  title: str
  artist_name: str
  url: str

  def __str__(self) -> str:
    return f'{self.artist_name} - {self.title}'