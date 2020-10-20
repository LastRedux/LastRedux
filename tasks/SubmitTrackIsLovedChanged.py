from loguru import logger
from PySide2 import QtCore

class SubmitTrackIsLovedChanged(QtCore.QRunnable): # Don't inherit from QObject because no signals are used
  def __init__(self, lastfm_instance, scrobble, is_loved):
    QtCore.QRunnable.__init__(self)
    self.lastfm_instance = lastfm_instance
    self.scrobble = scrobble
    self.is_loved = is_loved
    self.setAutoDelete(True)
  
  def run(self):
    self.lastfm_instance.set_track_is_loved(self.scrobble, self.is_loved)
    loguru.success(f'Set loved for {self.scrobble.title} to {self.is_loved}')