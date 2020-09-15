import os
import webbrowser

from PySide2 import QtCore, QtSql

import util.LastfmApiWrapper as lastfm

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
webbrowser.open(lastfm_instance.generate_authorization_url(auth_token))

# Wait for input
input('Hit enter after authorizing access to Last.fm in your web browser ')

# Get and save a new session key from Last.fm 
session_key, username = lastfm_instance.get_session_key_and_username(auth_token)
lastfm_instance.set_login_info(session_key, username)

print(f'Successfully logged in as {username} with {session_key}')

# Save session_key to db
session_key_query = QtSql.QSqlQuery()
session_key_query.prepare('INSERT INTO lastfm_login_info (key, value) VALUES ("session_key", :session_key)')
session_key_query.bindValue(':session_key', session_key)
session_key_query.exec_()

# Save username to db
username_query = QtSql.QSqlQuery()
username_query.prepare('INSERT INTO lastfm_login_info (key, value) VALUES ("username", :username)')
username_query.bindValue(':username', username)
username_query.exec_()

print(lastfm_instance.get_user_info())

# # Get user info from Last.fm
# real_name = user_info.get('realname')
# url = user_info['url']
# registered_timestamp = user_info['registered']['#text']
# image_url = user_info['image'][-2]['#text']

# # Set up the queries but don't run them
# query = QtSql.QSqlQuery()

# # Clear out the database
# query.prepare('DELETE FROM lastfm_data')
# query.exec_()

# # Save our values in the database
# query.prepare('INSERT INTO lastfm_data (key, value) VALUES \
# ("username", :username),\
# ("session_key", :session_key),\
# ("real_name", :real_name),\
# ("url", :url),\
# ("image_url", :image_url),\
# ("registered_timestamp", :registered_timestamp)')

# # .bindValue Automatically escapes the string
# query.bindValue(':username', username)
# query.bindValue(':session_key', session_key)
# query.bindValue(':real_name', real_name) # .get because it may not exist
# query.bindValue(':url', url)
# query.bindValue(':image_url', image_url) # Get large size
# query.bindValue(':registered_timestamp', registered_timestamp)

# # Run the query
# query.exec_()
