import logging
from util.lastfm.LastfmAlbum import LastfmAlbum
from util.lastfm.LastfmArtist import LastfmArtist

from PySide2 import QtCore

from util.lastfm import LastfmRequest, LastfmTrack
from datatypes.Scrobble import Scrobble

class LoadExternalScrobbleData(QtCore.QObject):#, QtCore.QRunnable):
  finished = QtCore.Signal(Scrobble)

  def __init__(self, scrobble: Scrobble):
    QtCore.QObject.__init__(self)
    # QtCore.QRunnable.__init__(self)
    
    self.scrobble = scrobble
    self.__items_left = 3
    # self.setAutoDelete(True)

  def run(self):
    lastfm_track_request = LastfmRequest()
    lastfm_track_request.finished.connect(lambda a: self.__handle_lastfm_track_fetched(a))
    lastfm_track_request.get_track_info(self.scrobble.artist_name, self.scrobble.track_title)
    
    lastfm_artist_request = LastfmRequest()
    lastfm_artist_request.finished.connect(lambda a: self.__handle_lastfm_artist_fetched(a))
    lastfm_artist_request.get_artist_info(self.scrobble.artist_name)
    
    lastfm_album_request = LastfmRequest()
    lastfm_album_request.finished.connect(lambda a: self.__handle_lastfm_album_fetched(a))
    lastfm_album_request.get_album_info(self.scrobble.artist_name, self.scrobble.album_title)

    # TODO: Fix error handling
    # lastfm_track = None 
    
    # try:
    #   lastfm_track = self.lastfm.get_track_info(
    #     artist_name=self.scrobble.artist_name,
    #     track_title=self.scrobble.track_title
    #   )
    # except Exception as err:
    #   self.scrobble.has_error = True
    #   logging.error(err)

  def __handle_lastfm_track_fetched(self, lastfm_track: LastfmTrack) -> None:
    print('t')
    self.scrobble.lastfm_track = lastfm_track

    self.__items_left -= 1

    if not self.__items_left:
      self.scrobble.is_loading = False
      self.finished.emit(self.scrobble)
  
  def __handle_lastfm_artist_fetched(self, lastfm_artist: LastfmArtist) -> None:
    print('a')
    self.scrobble.lastfm_artist = lastfm_artist

    self.__items_left -= 1

    if not self.__items_left:
      self.scrobble.is_loading = False
      self.finished.emit(self.scrobble)
  
  def __handle_lastfm_album_fetched(self, lastfm_album: LastfmAlbum) -> None:
    print('al')
    self.scrobble.lastfm_album = lastfm_album

    self.__items_left -= 1

    if not self.__items_left:
      self.scrobble.is_loading = False
      self.finished.emit(self.scrobble)