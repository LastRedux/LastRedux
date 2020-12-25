from dataclasses import dataclass

@dataclass
class LastfmAlbum:
  title: str
  artist_name: str
  url: str

  def __str__(self) -> str:
    return f'{self.title} | {self.artist_name}'