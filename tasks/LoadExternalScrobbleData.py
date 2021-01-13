from PySide2 import QtCore

from util.lastfm import LastfmApiWrapper
from util.AlbumArtProvider import AlbumArtProvider
from datatypes.Scrobble import Scrobble

class LoadExternalScrobbleData(QtCore.QObject, QtCore.QRunnable):
  update_ui_for_scrobble = QtCore.Signal(Scrobble)
  finished = QtCore.Signal()

  def __init__(self, lastfm: LastfmApiWrapper, art_provider: AlbumArtProvider, scrobble: Scrobble):
    QtCore.QObject.__init__(self)
    QtCore.QRunnable.__init__(self)
    self.lastfm = lastfm
    self.art_provider = art_provider
    self.scrobble = scrobble
    self.setAutoDelete(True)

  def run(self):
    '''Load Last.fm track + artist info, album art for scrobble and update the UI progressively'''

    # 1. Fetch and load Last.fm track info (first becuase we need is_loved value)
    self.scrobble.lastfm_track = self.lastfm.get_track_info(
      artist_name=self.scrobble.artist_name,
      track_title=self.scrobble.track_title
    )
    self.update_ui_for_scrobble.emit(self.scrobble)

    # 2. Fetch and load album art from whichever source is ideal
    self.scrobble.image_set = self.art_provider.get_album_art(
      artist_name=self.scrobble.artist_name,
      track_title=self.scrobble.track_title,
      album_title=self.scrobble.album_title
    )
    self.update_ui_for_scrobble.emit(self.scrobble)

    # 3. Fetch Last.fm artist info and replace basic artist info from track info request
    self.scrobble.lastfm_track.artist = self.lastfm.get_artist_info(self.scrobble.artist_name)
    self.update_ui_for_scrobble.emit(self.scrobble)

    self.finished.emit()