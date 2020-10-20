from loguru import logger
from PySide2 import QtSql

def connect():
  # Connect to SQLite for the first time
  db = QtSql.QSqlDatabase.addDatabase('QSQLITE')
  db.setDatabaseName('db.sqlite')

  # Open the database and log connection status
  if db.open():
    logger.success('sqlite connection succeeded')
  else:
    logger.critical('sqlite connection failed')

def get_lastfm_session_details():
  '''Fetch the user's Last.fm session key and username from the settings table'''
  
  # Execute SQL to find the row that matches our criteria
  username_query = QtSql.QSqlQuery('SELECT value FROM lastfm_login_info WHERE key="username"')

  # Move to next row and
  username_query.next()

  # Get column id for value in settings
  username = username_query.value(username_query.record().indexOf('value'))
  
  # Execute SQL to find the row that matches our criteria
  session_key_query = QtSql.QSqlQuery('SELECT value FROM lastfm_login_info WHERE key="session_key"')

  # Move to next row and 
  session_key_query.next()

  session_key = session_key_query.value(session_key_query.record().indexOf('value'))
  
  return session_key, username