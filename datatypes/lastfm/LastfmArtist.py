from dataclasses import dataclass

@dataclass
class LastfmArtist:
  name: str
  url: str

  def __str__(self) -> str:
    return self.name