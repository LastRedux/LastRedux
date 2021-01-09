from dataclasses import dataclass

@dataclass
class LastfmTag:
  name: str
  url: str

  def __str__(self) -> str:
    return self.name

  def __repr__(self) -> str:
    return str(self)