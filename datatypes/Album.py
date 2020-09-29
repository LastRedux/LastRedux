from dataclasses import dataclass

@dataclass
class Album:
  # Media player data
  title: str = ''

  # iTunes store data
  image_url: str = ''
  image_url_small: str = ''

  # Last.fm data
  lastfm_url: str = ''

  def load_lastfm_album_data(self, lastfm_album) -> None:
    self.lastfm_url = lastfm_album['url']
    self.image_url = lastfm_album['image'][4]['#text'] # Pick mega size in images array
    self.image_url_small = lastfm_album['image'][1]['#text'] # Pick medium size in images array