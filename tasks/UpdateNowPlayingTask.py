from PySide2 import QtCore

class UpdateNowPlayingTask(QtCore.QRunnable): # Don't inherit from QObject because no signals are used
  def __init__(self, lastfm_instance, scrobble):
    QtCore.QRunnable.__init__(self)
    self.lastfm_instance = lastfm_instance
    self.scrobble = scrobble
    self.setAutoDelete(True)
  
  def run(self):
    self.lastfm_instance.update_now_playing(self.scrobble)
    print(f'Updated now playing: {self.scrobble.track.title}')