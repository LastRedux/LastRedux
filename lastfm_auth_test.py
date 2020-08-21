import os

from PySide2 import QtCore, QtSql

import util.LastFmApiWrapper as lastfm

lastfm_instance = lastfm.get_static_instance()

# Db setup
db = QtSql.QSqlDatabase.addDatabase('QSQLITE')
db.setDatabaseName('db.sqlite')

if db.open():
  print('sqlite connection succeeded')
else:
  print('sqlite connection failed')

# Last.fm auth
auth_token = lastfm_instance.get_auth_token()

lastfm_instance.open_authorization_url(auth_token)

# Wait for input
input('Hit enter after authorizing access to Last.fm in your web browser ')

# Get session key from lastfm
username, session_key = lastfm_instance.get_new_session(auth_token)

username_query = QtSql.QSqlQuery()
session_key_query = QtSql.QSqlQuery()

# Set up the queries but don't run them
username_query.prepare('UPDATE settings SET stored_value = :username WHERE (setting = "username")')
session_key_query.prepare('UPDATE settings SET stored_value = :session_key WHERE (setting = "session_key")')

# Automatically escapes the string
username_query.bindValue(':username', username)
session_key_query.bindValue(':session_key', session_key)

# Run the queries
username_query.exec_()
session_key_query.exec_()

print(f'Welcome {username} ({session_key})')