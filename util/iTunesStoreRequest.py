import urllib
import json
import logging

from PySide2 import QtCore
from PySide2.QtNetwork import QNetworkRequest, QNetworkAccessManager, QNetworkReply

from datatypes.ImageSet import ImageSet

class iTunesStoreRequest(QtCore.QObject):
  finished = QtCore.Signal(ImageSet)

  def __init__(self, network_manager: QNetworkAccessManager) -> None:
    QtCore.QObject.__init__(self)
    self.__network_manager = network_manager
    self.__query: str = None
    self.__reply: QNetworkReply = None

  def get_album_art(
    self,
    artist_name: str,
    track_title: str,
    album_title: str=None
  ) -> None:
    '''Get album art for Apple Music tracks through the iTunes Search API'''

    # Escape special characters in query string
    self.__query = urllib.parse.quote(f'{artist_name} {track_title}')

    if album_title:
      self.__query += f' {album_title}'

    # Build the request url (must be a QUrl)
    url = QtCore.QUrl(
      f'https://itunes.apple.com/search?media=music&limit=1&term={self.__query}'
    )

    # Do a generic search for music with the track, artist, and album name
    self.__reply = self.__network_manager.get(QNetworkRequest(url))

    # Handle the response to the request
    # TODO: Figure out why passing the function directly doesn't work
    self.__reply.finished.connect(lambda: self.__handle_album_art_fetched())

  def __handle_album_art_fetched(self) -> None:
    if self.__reply.error() != QNetworkReply.NetworkError.NoError:
      logging.warning(
        f'Error searching iTunes store for "{self.__query}": {self.__reply.readAll()}'
      )

    reply_data = bytes(self.__reply.readAll()).decode()
    track_results = json.loads(reply_data)['results']

    # Return an empty object if there are no results for the track (local file)
    if not track_results:
      logging.warning(f'No iTunes Store results for "{self.__query}"')
      return

    image_set = ImageSet(
      small_url=track_results[0]['artworkUrl30'].replace('30x30', '64x64'),
      medium_url=track_results[0]['artworkUrl30'].replace('30x30', '300x300')
    )

    self.finished.emit(image_set)