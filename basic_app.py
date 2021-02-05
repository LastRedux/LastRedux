import sys
import signal

from PySide2 import QtCore, QtNetwork

from util.HTTPRequest import HTTPRequest
from util.lastfm.LastfmRequest import LastfmRequest
import util.db_helper as db_helper

class Example:
  def __init__(self):
    self.doRequest()

  def doRequest(self):
    db_helper.connect()
    session = db_helper.get_lastfm_session()

    LastfmRequest.log_in_with_session(session)

    request = LastfmRequest()
    request.finished.connect(lambda data: self.__handle_response(data))
    request.get_artist_info('Porter Robinson')

  def __handle_response(self, data):
    print(data)

    QtCore.QCoreApplication.quit()

if __name__ == '__main__':
  app = QtCore.QCoreApplication([])
  HTTPRequest.NETWORK_MANAGER = QtNetwork.QNetworkAccessManager()
  ex = Example()
  
  signal.signal(signal.SIGINT, signal.SIG_DFL)
  sys.exit(app.exec_())