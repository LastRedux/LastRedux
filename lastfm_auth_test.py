import os

from PySide2 import QtCore, QtSql

from models import Scrobble
from LastFmApiWrapper import LastFmApiWrapper

# Constants
API_KEY = os.environ['LASTREDUX_LASTFM_API_KEY']
CLIENT_SECRET = os.environ['LASTREDUX_LASTFM_CLIENT_SECRET']

# Db setup
db = QtSql.QSqlDatabase.addDatabase('QSQLITE')
db.setDatabaseName('db.sqlite')

if db.open():
  print('sqlite connection succeeded')
else:
  print('sqlite connection failed')

# Last.fm setup
lastfm = LastFmApiWrapper(API_KEY, CLIENT_SECRET)

# Execute SQL to find the row that matches our criteria
query = QtSql.QSqlQuery('SELECT value FROM settings WHERE key in ("session_key", "username")')

# Get column id for value in settings
idValue = query.record().indexOf("value")

# Get the value of the column of the row that we found
query.next()
session_key = query.value(idValue)

# Get next value from query
query.next()
username = query.value(idValue)

if session_key:
  print(f'Welcome back {username}')
else:
  # Last.fm auth
  auth_token = lastfm.get_auth_token()

  lastfm.open_authorization_url(auth_token)

  # Wait for input
  input('Hit enter after authorizing access to Last.fm in your web browser ')

  # Get session key from lastfm
  session = lastfm.get_new_session(auth_token)
  
  session_key = session['session_key']
  username = session['username']

  session_key_query = QtSql.QSqlQuery()
  username_query = QtSql.QSqlQuery()

  # Set up the queries but don't run it
  session_key_query.prepare('UPDATE settings SET value = :session_key WHERE (key = "session_key")')
  username_query.prepare('UPDATE settings SET value = :username WHERE (key = "username")')
  
  # Automatically escapes the string
  session_key_query.bindValue(':session_key', session_key)
  username_query.bindValue(':username', username)

  # Run the queries
  session_key_query.exec_()
  username_query.exec_()

  print(f'Welcome {username} ({session_key})')