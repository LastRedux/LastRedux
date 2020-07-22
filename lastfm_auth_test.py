import os

from PySide2 import QtCore, QtSql

from LastFmWrapper import LastFmWrapper

# Constants
API_KEY = os.environ['LASTREDUX_LASTFM_API_KEY']
CLIENT_SECRET = os.environ['LASTREDUX_LASTFM_CLIENT_SECRET']

# Db setup
db = QtSql.QSqlDatabase.addDatabase('QSQLITE')
db.setDatabaseName('db.sqlite')

# Last.fm setup
lastfm = LastFmWrapper(API_KEY, CLIENT_SECRET)

if db.open():
  print('connection succeeded')
else:
  print('connection failed')

# Execute SQL to find the row that matches our criteria
query = QtSql.QSqlQuery('SELECT value FROM settings WHERE key = ("session_key")')

# Get column id for value in settings
idValue = query.record().indexOf("value")

# Iterate through the list of results which only has one item
query.next()

# Get the value of the column of the row that we found
session_key = query.value(idValue)

print(session_key)

if session_key == '':
  # Last.fm auth
  auth_token = lastfm.get_auth_token()

  lastfm.open_authorization_url(auth_token)

  # Wait for input
  input()

  session_key = lastfm.get_session_key(auth_token)

  print(f'Session key: {session_key}')

  query = QtSql.QSqlQuery()

  # Set up the query but don't run it
  query.prepare('UPDATE settings SET value = :session_key WHERE (key = "session_key")')
  
  # Automatically escapes the string
  query.bindValue(':session_key', session_key)

  # Run the query
  query.exec_()

r = lastfm._LastFmWrapper__lastfm_request({
  'method': 'track.updateNowPlaying',
  'artist': 'nom',
  'track': 'start',
  'sk': session_key
}, http_method='POST')

print(r)