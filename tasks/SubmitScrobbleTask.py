import os

from PySide2 import QtCore

class SubmitScrobbleTask(QtCore.QRunnable): # Don't inherit from QObject because no signals are used
  def __init__(self, lastfm_instance, scrobble):
    QtCore.QRunnable.__init__(self)
    self.lastfm_instance = lastfm_instance
    self.scrobble = scrobble
    self.setAutoDelete(True)
  
  def run(self):
    if os.environ.get('MOCK'):
      print(f'MOCK submitted: {self.scrobble.track.title}')
      return

    self.lastfm_instance.submit_scrobble(self.scrobble)
    print(f'Submitted: {self.scrobble.track.title}')