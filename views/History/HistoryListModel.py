from PySide2 import QtCore

from ApplicationViewModel import ApplicationViewModel
from .HistoryViewModel import HistoryViewModel

class HistoryListModel(QtCore.QAbstractListModel):
  # Store role constants that are used as object keys in JS
  _TRACK_TITLE_ROLE = QtCore.Qt.UserRole # UserRole means custom role
  _ARTIST_NAME_ROLE = QtCore.Qt.UserRole + 1
  _TIMESTAMP_ROLE = QtCore.Qt.UserRole + 2
  _LASTFM_IS_LOVED_ROLE = QtCore.Qt.UserRole + 3
  _ALBUM_IMAGE_URL_ROLE = QtCore.Qt.UserRole + 4
  _HAS_LASTFM_DATA = QtCore.Qt.UserRole + 5

  def __init__(self, parent=None): # parent=None because it isn't within another list
    QtCore.QAbstractListModel.__init__(self, parent)

    self._application_reference = None
    self._history_reference = None
  
  def _scrobble_album_image_changed(self, row):
    '''Tell Qt that the scrobble album image has changed'''

    # Create a QModelIndex from the row index
    index = self.createIndex(row, 0)

    # Use list model dataChanged signal to indicate that UI needs to be updated at index
    self.dataChanged.emit(index, index, [self._ALBUM_IMAGE_URL_ROLE, self._HAS_LASTFM_DATA]) # index twice because start and end range

  def _scrobble_lastfm_is_loved_changed(self, row):
    '''Tell the Qt that the track loved status has changed'''

    index = self.createIndex(row, 0)
    self.dataChanged.emit(index, index, [self._LASTFM_IS_LOVED_ROLE])

  # --- Qt Property Getters and Setters ---

  def set_application_reference(self, new_reference: ApplicationViewModel) -> None:
    if not new_reference:
      return
    
    self._application_reference = new_reference

  def set_history_reference(self, new_reference: HistoryViewModel) -> None:
    # Only change the view model reference if there is a new one (don't reload when closing the app)
    if not new_reference:
      return

    # Tell the list model that the entirety of the list will be replaced (not just change one item)
    self.beginResetModel()
    self._history_reference: HistoryViewModel = new_reference
    self.endResetModel()
    
    # Tell Qt that a new row at the top of the list will be added
    self._history_reference.pre_append_scrobble.connect(lambda: self.beginInsertRows(QtCore.QModelIndex(), 0, 0)) # 0 and 0 are start and end indices

    # Tell Qt that a row has been added
    self._history_reference.post_append_scrobble.connect(lambda: self.endInsertRows())

    # Tell Qt that we are beginning and ending a full refresh of the model
    self._history_reference.begin_refresh_history.connect(lambda: self.beginResetModel())
    self._history_reference.end_refresh_history.connect(lambda: self.endResetModel())

    # Connect row data changed signals
    self._history_reference.scrobble_album_image_changed.connect(self._scrobble_album_image_changed)
    self._history_reference.scrobble_lastfm_is_loved_changed.connect(self._scrobble_lastfm_is_loved_changed)

  # --- QAbstractListModel Implementation ---

  def roleNames(self):
    '''Create a mapping of our enum ints to their JS object key names'''
    
    # Only the track title, artist name, and timestamp attributes of a scrobble will be displayed in scrobble history item views 
    # Use binary strings because C++ requires it
    return {
      self._TRACK_TITLE_ROLE: b'trackTitle',
      self._ARTIST_NAME_ROLE: b'artistName',
      self._ALBUM_IMAGE_URL_ROLE: b'albumImageUrl',
      self._LASTFM_IS_LOVED_ROLE: b'lastfmIsLoved',
      self._TIMESTAMP_ROLE: b'timestamp',
      self._HAS_LASTFM_DATA: b'hasLastfmData'
    }

  def rowCount(self, parent=QtCore.QModelIndex()):
    '''Return the number of rows in the scrobble history list''' 

    # Prevent value from being returned if the list has a parent (is inside another list)
    if self._application_reference and not parent.isValid():
      return len(self._application_reference.scrobble_history)

    return 0

  def data(self, index, role=QtCore.Qt.DisplayRole): # DisplayRole is a default role that returns the fallback value for the data function
    '''Provide data about items to each delegate view in the list'''

    if (
      not self._application_reference

      # Prevent checking for value if it's outside the current range of the list
      or not index.isValid()
    ):
      return

    scrobble = self._application_reference.scrobble_history[index.row()]

    if role == self._TRACK_TITLE_ROLE:
      return scrobble.track_title
    elif role == self._ARTIST_NAME_ROLE:
      return scrobble.artist_name
    elif role == self._ALBUM_IMAGE_URL_ROLE:
      return scrobble.image_set.small_url if scrobble.image_set else ''
    elif role == self._LASTFM_IS_LOVED_ROLE:
      return scrobble.lastfm_track.is_loved if scrobble.lastfm_track else False
    elif role == self._TIMESTAMP_ROLE:
      return scrobble.timestamp.strftime('%-m/%-d/%y %-I:%M:%S %p')
    elif role == self._HAS_LASTFM_DATA:
      return scrobble.lastfm_track is not None

    # Return no data if we don't have a reference to the scrobble history view model
    return None

  # --- Qt Properties ---

  applicationReference = QtCore.Property(
    type=ApplicationViewModel,
    fget=lambda self: self._application_reference,
    fset=set_application_reference
  )

  historyReference = QtCore.Property(
    type=HistoryViewModel,
    fget=lambda self: self._history_reference,
    fset=set_history_reference
  )
