import logging

from PySide2 import QtCore

from util.lastfm import LastfmApiWrapper

class UpdateNowPlaying(QtCore.QRunnable): # Don't inherit from QObject because no signals are used
  def __init__(
    self, 
    lastfm: LastfmApiWrapper,
    artist_name: str,
    track_title: str,
    album_title: str,
    duration: float
  ) -> None: 
    QtCore.QRunnable.__init__(self)
    self.lastfm = lastfm
    self.artist_name = artist_name
    self.track_title = track_title
    self.album_title = album_title
    self.duration = duration
    self.setAutoDelete(True)
  
  def run(self) -> None:
    self.lastfm.update_now_playing(
      artist_name=self.artist_name,
      track_title=self.track_title,
      album_title=self.album_title,
      duration=self.duration
    )
    
    logging.info(f'Updated now playing on Last.fm: {self.track_title}')