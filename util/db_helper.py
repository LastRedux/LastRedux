import sys

from loguru import logger
from PySide2 import QtCore, QtSql

from util.lastfm.LastfmSession import LastfmSession

def connect():
  # Connect to SQLite for the first time
  db = QtSql.QSqlDatabase.addDatabase('QSQLITE')

  if getattr(sys, 'frozen', False):
    db.setDatabaseName(QtCore.QDir.homePath() + '/LastRedux-db-private-beta-2.sqlite')
  else:
    db.setDatabaseName('db.sqlite')

  # Open the database and log connection status
  if db.open():
    logger.success('sqlite connection succeeded')
  else:
    logger.critical('sqlite connection failed')

def get_lastfm_session() -> LastfmSession:
  '''Fetch the user's Last.fm session key and username from the settings table'''
  
  # Execute SQL to find the row that matches our criteria
  username_query = QtSql.QSqlQuery('SELECT value FROM lastfm_login_info WHERE key="username"')

  # Move to next row
  if username_query.next():
    # Get column id for value in settings
    username = username_query.value(username_query.record().indexOf('value'))
    
    # Execute SQL to find the row that matches our criteria
    session_key_query = QtSql.QSqlQuery('SELECT value FROM lastfm_login_info WHERE key="session_key"')

    # Move to next row 
    session_key_query.next()

    session_key = session_key_query.value(session_key_query.record().indexOf('value'))
    
    return LastfmSession(session_key, username)

  return None

def create_lastfm_session_table():
  create_table_query = QtSql.QSqlQuery()
  create_table_query.exec_('CREATE TABLE lastfm_login_info(key text, value text)')
  
def save_lastfm_session_to_database(session: LastfmSession):
  # TODO: Only do this if there isn't already a table
  create_lastfm_session_table()

  # Insert session key
  session_key_insert_query = QtSql.QSqlQuery()
  session_key_insert_query.prepare('INSERT INTO lastfm_login_info (key, value) VALUES (:key, :value)')
  session_key_insert_query.bindValue(':key', 'session_key')
  session_key_insert_query.bindValue(':value', session.session_key)
  session_key_insert_query.exec_()

  # Insert username
  username_insert_query = QtSql.QSqlQuery()
  username_insert_query.prepare('INSERT INTO lastfm_login_info (key, value) VALUES (:key, :value)')
  username_insert_query.bindValue(':key', 'username')
  username_insert_query.bindValue(':value', session.username)
  username_insert_query.exec_()