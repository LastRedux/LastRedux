from PySide2 import QtCore

from util.lastfm import LastfmApiWrapper
from datatypes.Scrobble import Scrobble

class LoadLastfmAlbumInfo(QtCore.QObject, QtCore.QRunnable):
  finished = QtCore.Signal(Scrobble)

  def __init__(self, lastfm: LastfmApiWrapper, scrobble: Scrobble):
    QtCore.QObject.__init__(self)
    QtCore.QRunnable.__init__(self)
    self.lastfm = lastfm
    self.scrobble = scrobble
    self.setAutoDelete(True)

  def run(self):
    self.scrobble.lastfm_album = self.lastfm.get_album_info(
      artist_name=self.scrobble.album_artist_name or self.scrobble.artist_name,
      album_title=self.scrobble.album_title
    )
    self.finished.emit(self.scrobble)