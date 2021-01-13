from datatypes.Scrobble import Scrobble
from util.lastfm.LastfmApiWrapper import LastfmApiWrapper
from loguru import logger
from PySide2 import QtCore

class UpdateTrackLoveOnLastfm(QtCore.QRunnable):
  def __init__(self, lastfm: LastfmApiWrapper, scrobble: Scrobble, value: bool):
    QtCore.QRunnable.__init__(self)
    self.lastfm = lastfm
    self.scrobble = scrobble
    self.value = value
    self.setAutoDelete(True)
  
  def run(self):
    self.lastfm.set_track_is_loved(
      artist_name=self.scrobble.lastfm_track.artist.name,
      track_title=self.scrobble.lastfm_track.title,
      is_loved=self.value
    )

    logger.success(f'Track love updated on Last.fm: {self.scrobble} - {self.value}')