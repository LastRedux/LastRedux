from __future__ import annotations
from dataclasses import dataclass

@dataclass
class ProfileStatistic:
  title: str
  plays: int
  lastfm_url: str
  image_url: str
  has_image: bool = True
  subtitle: str = None
  secondary_lastfm_url: str = None
  percentage: float = None

  def __repr__(self) -> str:
    return f'{self.title} - {self.plays} plays'