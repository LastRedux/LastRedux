import os

from loguru import logger
from PySide2 import QtCore

from util.lastfm import LastfmApiWrapper
from datatypes import Scrobble

class SubmitScrobble(QtCore.QRunnable): # Don't inherit from QObject because no signals are used
  def __init__(self, lastfm: LastfmApiWrapper, scrobble: Scrobble):
    QtCore.QRunnable.__init__(self)
    self.lastfm = lastfm
    self.scrobble = scrobble
    self.setAutoDelete(True)
  
  def run(self):
    if os.environ.get('MOCK'):
      logger.success(f'MOCK submitted: {self.scrobble.title}')
      return

    self.lastfm.submit_scrobble(
      artist_name=self.scrobble.artist_name,
      track_title=self.scrobble.track_title,
      album_title=self.scrobble.album_title,
      date=self.scrobble.timestamp
    )
    logger.success(f'Submitted to Last.fm: {self.scrobble.track_title}')