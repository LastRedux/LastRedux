from PySide2 import QtCore

from datatypes.Track import Track

class FetchFriendTrackImage(QtCore.QObject, QtCore.QRunnable):
  finished = QtCore.Signal(int)

  def __init__(self, track: Track, row_in_friends_list: int):
    QtCore.QObject.__init__(self)
    QtCore.QRunnable.__init__(self)
    self.track = track
    self.setAutoDelete(True)
    self.row_in_friends_list = row_in_friends_list

  def run(self):
    '''Fetch and attach information from Last.fm and iTunes to the passed Track object '''

    self.track.load_lastfm_data(no_artists=True)

    if not self.track.album.image_url:
      self.track.load_spotify_data(no_artists=True)

    if not self.track.album.image_url:
      self.track.fetch_and_load_itunes_store_images()
      
    self.finished.emit(self.row_in_friends_list)