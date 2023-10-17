import sys
import logging

from PySide6 import QtCore, QtSql

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
    logging.info('sqlite connection succeeded')
  else:
    logging.critical('sqlite connection failed')

def get_lastfm_session() -> LastfmSession:
  '''Fetch the user's Last.fm session key and username from the settings table'''
  
  # Execute SQL to find the row that matches our criteria
  query = QtSql.QSqlQuery('SELECT value FROM lastfm_login_info WHERE key="username"')

  # Move to next row
  if query.next():
    # Get column id for value in settings
    username = query.value(query.record().indexOf('value'))
    
    # Execute SQL to find the row that matches our criteria
    query = QtSql.QSqlQuery('SELECT value FROM lastfm_login_info WHERE key="session_key"')

    # Move to next row 
    query.next()

    session_key = query.value(query.record().indexOf('value'))
    
    return LastfmSession(session_key, username)

  return None

def get_preference(key: str) -> any:
  query = QtSql.QSqlQuery()
  query.prepare('SELECT value FROM preferences WHERE key=:key')
  query.bindValue(':key', key)
  query.exec_()

  if query.next():
    value = query.value(query.record().indexOf('value'))

    if value == 'true':
      return True
    
    if value == 'false':
      return False
    
    return value
  
  logging.error(f'Cannot fetch value in preferences table for {key}')

def set_preference(key: str, value: any):
  query = QtSql.QSqlQuery()
  query.prepare('UPDATE preferences SET value = :value WHERE key = :key')

  if value == True:
    query.bindValue(':value', 'true')
  elif value == False:
    query.bindValue(':value', 'false')
  else:
    query.bindValue(':value', value)

  query.bindValue(':key', key)
  query.exec_()

def create_lastfm_session_table():
  create_table_query = QtSql.QSqlQuery()
  create_table_query.exec_('CREATE TABLE lastfm_login_info(key text, value text)')

def create_preferences_table():
  create_table_query = QtSql.QSqlQuery()
  create_table_query.exec_('CREATE TABLE preferences(key text, value text)')
  
def save_lastfm_session_to_database(session: LastfmSession):
  # TODO: Only do this if there isn't already a table
  create_lastfm_session_table()

  # Insert session key
  insert_query = QtSql.QSqlQuery()
  insert_query.prepare('INSERT INTO lastfm_login_info (key, value) VALUES (:key, :value)')
  insert_query.bindValue(':key', 'session_key')
  insert_query.bindValue(':value', session.session_key)
  insert_query.exec_()

  # Insert username
  insert_query.prepare('INSERT INTO lastfm_login_info (key, value) VALUES (:key, :value)')
  insert_query.bindValue(':key', 'username')
  insert_query.bindValue(':value', session.username)
  insert_query.exec_()

def save_default_preferences_to_database(media_player_preference: str):
  create_preferences_table()

  # Set up preferences with default values
  insert_query = QtSql.QSqlQuery()
  insert_query.prepare('INSERT INTO preferences (key, value) VALUES ("rich_presence_enabled", "false")')
  insert_query.exec_()
  insert_query.prepare('INSERT INTO preferences (key, value) VALUES ("is_in_mini_mode", "false")')
  insert_query.exec_()
  insert_query.prepare('INSERT INTO preferences (key, value) VALUES ("media_player", :value)')
  insert_query.bindValue(':value', media_player_preference)
  insert_query.exec_()