from __future__ import annotations
from dataclasses import dataclass

@dataclass
class ProfileStatistic:
  title: str
  subtitle: str
  plays: int
  percentage: float
  lastfm_url: str
  secondary_lastfm_url: str
  image_url: str
  has_image: bool = True