from PySide2 import QtCore

from util.AlbumArtProvider import AlbumArtProvider
from datatypes import FriendScrobble

class FetchFriendScrobbleArt(QtCore.QObject, QtCore.QRunnable):
  finished = QtCore.Signal(int)

  def __init__(self, album_art_provider: AlbumArtProvider, friend_scrobble: FriendScrobble, row_in_friends_list: int):
    QtCore.QObject.__init__(self)
    QtCore.QRunnable.__init__(self)
    self.album_art_provider = album_art_provider
    self.friend_scrobble = friend_scrobble
    self.setAutoDelete(True)
    self.row_in_friends_list = row_in_friends_list

  def run(self):
    '''Fetch album art for the passed FriendScrobble'''

    album_art = self.album_art_provider.get_album_art(
      artist_name=self.friend_scrobble.artist_name,
      track_title=self.friend_scrobble.track_title,
      album_title=self.friend_scrobble.album_title,
    )
    self.friend_scrobble.image_url = album_art.medium_url

    self.finished.emit(self.row_in_friends_list)