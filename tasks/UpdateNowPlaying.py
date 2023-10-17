import logging

from PySide6 import QtCore

from util.lastfm import LastfmApiWrapper

class UpdateNowPlaying(QtCore.QRunnable): # Don't inherit from QObject because no signals are used
  def __init__(
    self, 
    lastfm: LastfmApiWrapper,
    artist_name: str,
    track_title: str,
    duration: float,
    album_title: str,
    album_artist_name: str
  ) -> None:
    QtCore.QRunnable.__init__(self)
    self.lastfm = lastfm
    self.artist_name = artist_name
    self.track_title = track_title
    self.duration = duration
    self.album_title = album_title
    self.album_artist_name = album_artist_name
    self.setAutoDelete(True)
  
  def run(self) -> None:
    self.lastfm.update_now_playing(
      artist_name=self.artist_name,
      track_title=self.track_title,
      duration=self.duration,
      album_title=self.album_title,
      album_artist_name=self.album_artist_name
    )
    
    logging.info(f'Now playing updated to "{self.track_title}" on Last.fm')