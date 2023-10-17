import logging

from PySide6 import QtCore

from util.lastfm import LastfmApiWrapper
from datatypes.Scrobble import Scrobble

class LoadLastfmTrackInfo(QtCore.QObject, QtCore.QRunnable):
  finished = QtCore.Signal(Scrobble)

  def __init__(self, lastfm: LastfmApiWrapper, scrobble: Scrobble):
    QtCore.QObject.__init__(self)
    QtCore.QRunnable.__init__(self)
    self.lastfm = lastfm
    self.scrobble = scrobble
    self.setAutoDelete(True)

  def run(self):
    lastfm_track = None
    
    try:
      lastfm_track = self.lastfm.get_track_info(
        artist_name=self.scrobble.artist_name,
        track_title=self.scrobble.track_title
      )
    except Exception as err:
      self.scrobble.has_error = True
      logging.warning(err)

    self.scrobble.lastfm_track = lastfm_track # Could be None
    self.finished.emit(self.scrobble)