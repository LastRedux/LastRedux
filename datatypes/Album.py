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

  def load_lastfm_images(self, lastfm_images) -> None:
    self.image_url = lastfm_images[-1]['#text'] # -1 is largest size
    self.image_url_small = lastfm_images[1]['#text'] # 1 is medium size
  
  def load_lastfm_album_data(self, lastfm_album) -> None:
    self.lastfm_url = lastfm_album['url']
    self.load_lastfm_images(lastfm_album['image'])
    
  def load_lastfm_track_images(self, lastfm_track) -> None:
    self.load_lastfm_images(lastfm_track['album']['image'])