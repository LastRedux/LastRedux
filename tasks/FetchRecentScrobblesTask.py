from PySide2 import QtCore

class FetchRecentScrobblesTask(QtCore.QObject, QtCore.QRunnable):
  finished = QtCore.Signal(list)

  def __init__(self, lastfm_instance, count):
    QtCore.QObject.__init__(self)
    QtCore.QRunnable.__init__(self)
    self.lastfm_instance = lastfm_instance
    self.setAutoDelete(True)
    self.count = count

  def run(self):
    '''Return recent Last.fm scrobbles'''

    recent_scrobbles = self.lastfm_instance.get_recent_scrobbles(count=self.count)
    self.finished.emit(recent_scrobbles['recenttracks']['track'])