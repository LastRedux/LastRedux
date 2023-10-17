from typing import List

from PySide6 import QtCore

from util.spotify_api import SpotifyApiWrapper
from datatypes.ProfileStatistic import ProfileStatistic

class LoadProfileSpotifyArtists(QtCore.QObject, QtCore.QRunnable):
  finished = QtCore.Signal()

  def __init__(self, spotify_api: SpotifyApiWrapper, top_artists: List[ProfileStatistic]) -> None:
    QtCore.QObject.__init__(self)
    QtCore.QRunnable.__init__(self)
    self.spotify_api = spotify_api
    self.top_artists = top_artists
    self.setAutoDelete(True)

  def run(self) -> None:
    '''Load Spotify data into top artists'''

    for top_artist in self.top_artists:
      spotify_artist = self.spotify_api.get_artist(top_artist.title)

      if spotify_artist:
        top_artist.image_url = spotify_artist.image_url

    self.finished.emit()