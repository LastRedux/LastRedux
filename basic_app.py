import sys
import logging
import signal
import webbrowser

from PySide2 import QtCore, QtNetwork
from rich.console import Console

from util.HTTPRequest import HTTPRequest
from util.lastfm.LastfmRequest import LastfmRequest
import util.db_helper as db_helper

class Example:
  def __init__(self):
    db_helper.connect()

  def do_authentication(self) -> None:
    session = db_helper.get_lastfm_session()

    if session:
      LastfmRequest.log_in_with_session(session)
      logging.info(f'Logged in from database as {session.username} with {session.session_key}')
    else:
      logging.info('\n***** GET AUTH TOKEN *****\n')
      request = LastfmRequest()
      request.finished.connect(lambda auth_token: self.__handle_auth_token_fetched)
      request.get_auth_token()
      
      # auth_token = lastfm.get_auth_token()
      # logging.info(f'Token: {auth_token}')

      # logging.info('\n***** AUTHORIZE ACCOUNT ACCESS *****\n')
      # webbrowser.open(lastfm.generate_authorization_url(auth_token))
      # input('(HIT ENTER TO CONTINUE)')

      # print('\n***** GET SESSION *****\n')

      # try:
      #   session = lastfm.get_session(auth_token)
      #   lastfm.log_in_with_session(session)
      #   logging.info(f'Successfully logged in as {session.username} with {session.session_key}')
      #   db_helper.save_lastfm_session_to_database(session)
      #   logging.info('Successfully saved session key and username to database')
      # except:
      #   logging.info(f'Could not get session, auth token not authorized')
      #   sys.exit(1)

    LastfmRequest.log_in_with_session(session)

    request = LastfmRequest()
    request.finished.connect(lambda data: self.__handle_response(data))
    request.get_recent_scrobbles()

  # --- Private Methods ---
  
  def __handle_auth_token_fetched(self, auth_token: str):
    pass

  def __handle_response(self, data):
    print(data)

    QtCore.QCoreApplication.quit()

if __name__ == '__main__':
  app = QtCore.QCoreApplication([])
  HTTPRequest.NETWORK_MANAGER = QtNetwork.QNetworkAccessManager()
  ex = Example()
  
  signal.signal(signal.SIGINT, signal.SIG_DFL)
  sys.exit(app.exec_())