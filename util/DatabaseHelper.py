from PySide2 import QtSql

class DatabaseHelper:
  def __init__(self, filename):
    # Connect to SQLite
    self.db = QtSql.QSqlDatabase.addDatabase('QSQLITE')
    self.db.setDatabaseName(filename)
   
    if self.db.open():
      print('sqlite connection succeeded')
    else:
      print('sqlite connection failed')

  def get_lastfm_session_details(self):
    '''Fetch the user's Last.fm session key and username from the settings table'''
    
    # Execute SQL to find the row that matches our criteria
    query = QtSql.QSqlQuery('SELECT value FROM settings WHERE key in ("username", "session_key")')

    # Get column id for value in settings
    idValue = query.record().indexOf('value')

    # Iterate through the list of results to get the first item, session_key
    query.next()

    username = query.value(idValue)

    # Iterate through the list of results to get the second item, username
    query.next()
    session_key = query.value(idValue)
    
    return username, session_key