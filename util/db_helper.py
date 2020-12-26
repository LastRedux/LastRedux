import os
import sys

from loguru import logger
from PySide2 import QtSql

def connect():
  # Connect to SQLite for the first time
  db = QtSql.QSqlDatabase.addDatabase('QSQLITE')

  if getattr(sys, 'frozen', False):
    db.setDatabaseName(os.path.dirname(sys.executable) + '/db.sqlite')
  else:
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

  # Move to next row
  if username_query.next():
    # Get column id for value in settings
    username = username_query.value(username_query.record().indexOf('value'))
    
    # Execute SQL to find the row that matches our criteria
    session_key_query = QtSql.QSqlQuery('SELECT value FROM lastfm_login_info WHERE key="session_key"')

    # Move to next row 
    session_key_query.next()

    session_key = session_key_query.value(session_key_query.record().indexOf('value'))
    
    return session_key, username

  return None, None

def create_lastfm_session_details(session_key, username):
  # Create lastfm_login_info table
  create_table_query = QtSql.QSqlQuery()
  create_table_query.exec_('CREATE TABLE lastfm_login_info(key text, value text)')

  # Insert session key
  session_key_insert_query = QtSql.QSqlQuery()
  session_key_insert_query.prepare('INSERT INTO lastfm_login_info (key, value) VALUES (:key, :value)')
  session_key_insert_query.bindValue(':key', 'session_key')
  session_key_insert_query.bindValue(':value', session_key)
  session_key_insert_query.exec_()

  # Insert username
  username_insert_query = QtSql.QSqlQuery()
  username_insert_query.prepare('INSERT INTO lastfm_login_info (key, value) VALUES (:key, :value)')
  username_insert_query.bindValue(':key', 'username')
  username_insert_query.bindValue(':value', username)
  username_insert_query.exec_()