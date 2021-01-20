from loguru import logger
from PySide2 import QtCore

from util.lastfm import LastfmApiWrapper
from datatypes.Scrobble import Scrobble

class UpdateNowPlaying(QtCore.QRunnable): # Don't inherit from QObject because no signals are used
  def __init__(self, lastfm: LastfmApiWrapper, scrobble: Scrobble, duration: float):
    QtCore.QRunnable.__init__(self)
    self.lastfm = lastfm
    self.scrobble = scrobble
    self.duration = duration
    self.setAutoDelete(True)
  
  def run(self):
    self.lastfm.update_now_playing(
      artist_name=self.scrobble.artist_name,
      track_title=self.scrobble.track_title,
      album_title=self.scrobble.album_title,
      duration=self.duration
    )
    logger.success(f'Updated now playing on Last.fm: {self.scrobble.track_title}')