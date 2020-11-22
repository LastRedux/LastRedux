from __future__ import annotations # For self-referential return type
from dataclasses import dataclass

@dataclass
class ListeningStatistic:
  title: str
  plays: int
  lastfm_url: str
  image_url: str
  has_image: bool
  subtitle: str = None
  plays_percentage: float = None

  @staticmethod
  def build_from_artist(lastfm_artist):
    return ListeningStatistic(
      title=lastfm_artist['name'],
      plays=int(lastfm_artist['playcount']),
      lastfm_url=lastfm_artist['url'],
      image_url=lastfm_artist['image'][2]['#text'],
      has_image=True#False
    )

  @staticmethod
  def build_from_track(lastfm_track):
    return ListeningStatistic(
      title=lastfm_track['name'],
      plays=int(lastfm_track['playcount']),
      lastfm_url=lastfm_track['url'],
      image_url=lastfm_track['image'][2]['#text'], # Get medium size
      has_image=True
    )

  @staticmethod
  def build_from_album(lastfm_album):
    return ListeningStatistic(
      title=lastfm_album['name'],
      plays=int(lastfm_album['playcount']),
      lastfm_url=lastfm_album['url'],
      image_url=lastfm_album['image'][2]['#text'], # Get medium size
      has_image=True
    )