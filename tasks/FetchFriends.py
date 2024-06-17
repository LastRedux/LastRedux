from PySide6 import QtCore

from util.lastfm import LastfmApiWrapper


class FetchFriends(QtCore.QObject, QtCore.QRunnable):
    """
    Signal emitted when the request finishes with the list of Last.fm users and whether there was an error
    """

    finished = QtCore.Signal(list, bool)

    def __init__(self, lastfm: LastfmApiWrapper):
        QtCore.QObject.__init__(self)
        QtCore.QRunnable.__init__(self)
        self.lastfm = lastfm
        self.setAutoDelete(True)

    def run(self) -> None:
        try:
            friends = self.lastfm.get_friends()
            self.finished.emit(friends, False)
        except:
            self.finished.emit(None, True)
