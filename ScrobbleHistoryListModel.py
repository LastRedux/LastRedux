from PySide2 import QtCore

from ScrobbleHistoryViewModel import ScrobbleHistoryViewModel

class ScrobbleHistoryListModel(QtCore.QAbstractListModel):
  # Store role constants that are used as object keys in JS
  __NAME_ROLE = QtCore.Qt.UserRole # UserRole means custom role
  __ARTIST_ROLE = QtCore.Qt.UserRole + 1
  __TIMESTAMP_ROLE = QtCore.Qt.UserRole + 2
  __IS_LOVED_ROLE = QtCore.Qt.UserRole + 3
  __ALBUM_IMAGE_URL_ROLE = QtCore.Qt.UserRole + 4
  __IS_ADDITIONAL_DATA_DOWNLOADED_ROLE = QtCore.Qt.UserRole + 5

  def __init__(self, parent=None):
    QtCore.QAbstractListModel.__init__(self, parent)

    # Store reference to application view model
    self.__scrobble_history_reference = None
  
  def __scrobble_album_image_changed(self, row):
    # Create a QModelIndex from the row index
    index = self.createIndex(row, 0)

    # Use list model dataChanged signal to indicate that UI needs to be updated at index
    self.dataChanged.emit(index, index, [self.__ALBUM_IMAGE_URL_ROLE, self.__IS_ADDITIONAL_DATA_DOWNLOADED_ROLE]) # index twice because start and end range

  # --- Qt Property Getters and Setters ---

  def get_scrobble_history_reference(self):
    return self.__scrobble_history_reference

  def set_scrobble_history_reference(self, new_reference):
    # Only change the view model reference if there is a new one (don't reload when closing the app)
    if new_reference:
      # Tell the list model that the entirety of the list will be replaced (not just change one item)
      self.beginResetModel()
      self.__scrobble_history_reference = new_reference
      self.endResetModel()
      
      # Tell Qt that a new row at the top of the list will be added
      self.__scrobble_history_reference.pre_append_scrobble.connect(lambda: self.beginInsertRows(QtCore.QModelIndex(), 0, 0)) # 0 and 0 are start and end indices

      # Tell Qt that a row has been added
      self.__scrobble_history_reference.post_append_scrobble.connect(lambda: self.endInsertRows())

      # Tell Qt that the scrobble image has changed
      self.__scrobble_history_reference.scrobble_album_image_changed.connect(self.__scrobble_album_image_changed)

  # --- QAbstractListModel Implementation ---

  def roleNames(self):
    '''Create a mapping of our enum ints to their JS object key names'''
    
    # Only the name, artist, and timestamp attributes of a scrobble will be displayed in scrobble history item views 
    # Use binary strings because C++ requires it
    return {
      self.__NAME_ROLE: b'name',
      self.__ARTIST_ROLE: b'artist',
      self.__ALBUM_IMAGE_URL_ROLE: b'albumImageUrl',
      self.__IS_LOVED_ROLE: b'isLoved',
      self.__TIMESTAMP_ROLE: b'timestamp',
      self.__IS_ADDITIONAL_DATA_DOWNLOADED_ROLE: b'isAdditionalDataDownloaded'
    }

  def rowCount(self, parent=QtCore.QModelIndex()):
    '''Return the number of rows in the scrobble history list'''

    # Prevent value from being returned if the list has a parent (is inside another list)
    if self.__scrobble_history_reference and not parent.isValid():
      return len(self.__scrobble_history_reference.scrobble_history)

    return 0

  def data(self, index, role=QtCore.Qt.DisplayRole): # DisplayRole is a default role that returns the fallback value for the data function
    '''Provide data about items to each delegate view in the list'''

    if self.__scrobble_history_reference:
      # Only check for value if it's in the current range of the list
      if index.isValid():
        scrobble = self.__scrobble_history_reference.scrobble_history[index.row()]

        if role == self.__NAME_ROLE:
          return scrobble.track['name']
        elif role == self.__ARTIST_ROLE:
          return scrobble.track['artist']['name']
        elif role == self.__ALBUM_IMAGE_URL_ROLE:
          return scrobble.track['album']['image_url_small']
        elif role == self.__IS_LOVED_ROLE:
          return scrobble.track['is_loved']
        elif role == self.__TIMESTAMP_ROLE:
          return scrobble.timestamp.strftime('%-m/%-d/%y %-I:%M:%S %p')
        elif role == self.__IS_ADDITIONAL_DATA_DOWNLOADED_ROLE:
          return scrobble.track['is_additional_data_downloaded']

    # Return no data if we don't have a reference to the scrobble history view model
    return None

  # --- Qt Properties ---

  # Allow the __scrobble_history_reference to be set in the view
  scrobbleHistoryReference = QtCore.Property(ScrobbleHistoryViewModel, get_scrobble_history_reference, set_scrobble_history_reference)
