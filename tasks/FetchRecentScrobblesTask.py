import os
from util.lastfm.LastfmList import LastfmList

from PySide2 import QtCore

from util.helpers import get_mock_recent_scrobbles
from util.lastfm import LastfmApiWrapper

class FetchRecentScrobblesTask(QtCore.QObject, QtCore.QRunnable):
  finished = QtCore.Signal(LastfmList)

  def __init__(self, lastfm: LastfmApiWrapper, count: int) -> None:
    QtCore.QObject.__init__(self)
    QtCore.QRunnable.__init__(self)
    self.lastfm = lastfm
    self.count = count
    self.setAutoDelete(True)

  def run(self) -> None:

    recent_scrobbles = None

    if os.environ.get('MOCK'):
      recent_scrobbles = get_mock_recent_scrobbles(self.count)
    else:
      recent_scrobbles = self.lastfm.get_recent_scrobbles(self.count)
    
    self.finished.emit(recent_scrobbles)