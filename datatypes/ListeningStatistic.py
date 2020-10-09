from __future__ import annotations # For self-referential return type
from dataclasses import dataclass

@dataclass
class ListeningStatistic:
  title: str
  subtitle: str
  percentage: float
  lastfm_plays: int
  lastfm_url: str
  image_url: str
  has_image: bool

  @staticmethod
  def build_from_artist(lastfm_artist) -> Artist:
    return ListeningStatistic(
      title=lastfm_artist['name'],
      subtitle='',
      percentage=0.0,
      lastfm_plays=int(lastfm_artist['playcount']),
      lastfm_url=lastfm_artist['url'],
      image_url='',
      has_image=False
    )