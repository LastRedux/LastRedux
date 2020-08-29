from PySide2 import QtCore

class FetchRecentScrobblesTask(QtCore.QObject, QtCore.QRunnable):
  finished = QtCore.Signal(list)

  def __init__(self, lastfm_instance):
    QtCore.QObject.__init__(self)
    QtCore.QRunnable.__init__(self)
    self.lastfm_instance = lastfm_instance
    self.setAutoDelete(True)

  def run(self):
    '''Return recent Last.fm scrobbles'''

    recent_lastfm_scrobbles = self.lastfm_instance.get_recent_scrobbles()['recenttracks']['track']
    self.finished.emit(recent_lastfm_scrobbles)
    self.finished.emit(recent_lastfm_scrobbles)