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
  secondary_lastfm_url: str = None
  plays_percentage: float = None

  @staticmethod
  def build_from_artist(lastfm_artist) -> ListeningStatistic:
    return ListeningStatistic(
      title=lastfm_artist['name'],
      plays=int(lastfm_artist['playcount']),
      lastfm_url=lastfm_artist['url'],
      image_url=lastfm_artist['image'][2]['#text'],
      has_image=False
    )

  @staticmethod
  def build_from_track(lastfm_track) -> ListeningStatistic:
    return ListeningStatistic(
      title=lastfm_track['name'],
      subtitle=lastfm_track['artist']['name'],
      secondary_lastfm_url=lastfm_track['artist']['url'],
      plays=int(lastfm_track['playcount']),
      lastfm_url=lastfm_track['url'],
      image_url=lastfm_track['image'][2]['#text'], # Get medium size
      has_image=False
    )

  @staticmethod
  def build_from_album(lastfm_album) -> ListeningStatistic:
    return ListeningStatistic(
      title=lastfm_album['name'],
      subtitle=lastfm_album['artist']['name'],
      secondary_lastfm_url=lastfm_album['artist']['url'],
      plays=int(lastfm_album['playcount']),
      lastfm_url=lastfm_album['url'],
      image_url=lastfm_album['image'][2]['#text'], # Get medium size

      # TODO: Turn this back on when full art fetching logic is implemented
      has_image=False#True
    )