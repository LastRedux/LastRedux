from PySide6 import QtCore

from util.lastfm import LastfmApiWrapper
from datatypes.Scrobble import Scrobble


class LoadLastfmArtistInfo(QtCore.QObject, QtCore.QRunnable):
    finished = QtCore.Signal(Scrobble)

    def __init__(self, lastfm: LastfmApiWrapper, scrobble: Scrobble):
        QtCore.QObject.__init__(self)
        QtCore.QRunnable.__init__(self)
        self.lastfm = lastfm
        self.scrobble = scrobble
        self.setAutoDelete(True)

    def run(self):
        self.scrobble.lastfm_artist = self.lastfm.get_artist_info(
            self.scrobble.artist_name
        )
        self.finished.emit(self.scrobble)
