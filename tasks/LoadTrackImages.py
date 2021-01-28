from PySide2 import QtCore

from util.lastfm import LastfmApiWrapper
from util.art_provider import ArtProvider
from datatypes.Scrobble import Scrobble

class LoadTrackImages(QtCore.QObject, QtCore.QRunnable):
  finished = QtCore.Signal(Scrobble)

  def __init__(self, lastfm: LastfmApiWrapper, art_provider: ArtProvider, scrobble: Scrobble):
    QtCore.QObject.__init__(self)
    QtCore.QRunnable.__init__(self)
    self.lastfm = lastfm
    self.art_provider = art_provider
    self.scrobble = scrobble
    self.setAutoDelete(True)
  
  def run(self):
    scrobble_images = self.art_provider.get_scrobble_images(
      artist_name=self.scrobble.artist_name,
      track_title=self.scrobble.track_title,
      album_title=self.scrobble.album_title
    )
    self.scrobble.image_set = scrobble_images.album_art
    self.scrobble.spotify_artists = scrobble_images.spotify_artists
    self.finished.emit(self.scrobble)