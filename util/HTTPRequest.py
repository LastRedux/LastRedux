import json
import logging
import urllib.parse

from PySide2 import QtCore
from PySide2.QtNetwork import QNetworkRequest, QNetworkAccessManager, QNetworkReply

class HTTPRequest(QtCore.QObject):
  finished = QtCore.Signal(dict)

  NETWORK_MANAGER: QNetworkAccessManager

  def __init__(
    self,
    url: str,
    headers: dict=None,
    data: dict=None,
    http_method: str='GET'
  ) -> None:
    QtCore.QObject.__init__(self)

    self.url = url
    self.headers = headers
    self.data = data
    self.http_method = http_method

    self.__reply: QNetworkReply = None

  def run(self) -> None:
    url = self.url

    # Add query string to url for GET requests
    if self.data and self.http_method == 'GET':
      # Generate request url
      url += '?'
      url += urllib.parse.urlencode(self.data)

    # Create request
    request = QNetworkRequest(QtCore.QUrl(url))

    # Add headers
    if self.headers:
      for key, value in self.headers.items():
        request.setHeader(key, value)

    if self.http_method == 'GET':
      # Make GET request
      self.__reply = self.NETWORK_MANAGER.get(request)
    elif self.http_method == 'POST':
      # Convert args dict to url encoded data
      post_data = bytes(urllib.parse.urlencode(self.data), encoding='utf-8')
      
      # Set header to form encoding
      request.setHeader(QNetworkRequest.ContentTypeHeader, 'application/x-www-form-encoded')

      # Make POST request
      self.__reply = self.NETWORK_MANAGER.post(request, post_data)
    else:
      raise Exception('Invalid http method')
    
    # Handle the response to the request
    # TODO: Figure out why passing the function directly doesn't work
    self.__reply.finished.connect(lambda: self.__handle_reply())

  def __handle_reply(self) -> None:
    if self.__reply.error() != QNetworkReply.NetworkError.NoError:
      logging.warning(
        f'Error requesting "{self.url}" with "{self.data}": {self.__reply.readAll()}'
      )

      return

    reply_data = bytes(self.__reply.readAll()).decode()
    
    resp_json = None

    try:
      resp_json = json.loads(reply_data)
    except json.decoder.JSONDecodeError:
      logging.warning(
        f'Non-JSON respone "{self.url}" with "{self.data}": {self.__reply.readAll()}'
      )

    self.finished.emit(resp_json)