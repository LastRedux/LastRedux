from typing import Union

from PySide2 import QtCore

from .FriendsViewModel import FriendsViewModel

class FriendsListModel(QtCore.QAbstractListModel):
  _URL_ROLE = QtCore.Qt.UserRole
  _USERNAME_ROLE = QtCore.Qt.UserRole + 1
  _REAL_NAME_ROLE = QtCore.Qt.UserRole + 2
  _IMAGE_URL_ROLE = QtCore.Qt.UserRole + 3
  _TRACK_TITLE_ROLE = QtCore.Qt.UserRole + 4
  _TRACK_ARTIST_NAME_ROLE = QtCore.Qt.UserRole + 5
  _TRACK_URL_ROLE = QtCore.Qt.UserRole + 6
  _TRACK_ARTIST_URL_ROLE = QtCore.Qt.UserRole + 7
  _TRACK_IMAGE_URL = QtCore.Qt.UserRole + 8
  _IS_TRACK_PLAYING_ROLE = QtCore.Qt.UserRole + 9
  _IS_TRACK_LOVED_ROLE = QtCore.Qt.UserRole + 10
  _IS_LOADING_ROLE = QtCore.Qt.UserRole + 11

  def __init__(self, parent=None):
    QtCore.QAbstractListModel.__init__(self, parent)

    self._friends_reference = None

  # --- Qt Property Getters and Setters ---

  def get_friends_reference(self) -> None:
    return self._friends_reference

  def set_friends_reference(self, newReference: FriendsViewModel) -> None:
    if newReference:
      self.beginResetModel()
      self._friends_reference = newReference
      self.endResetModel()

      self._friends_reference.begin_refresh_friends.connect(lambda: self.beginResetModel())
      self._friends_reference.end_refresh_friends.connect(lambda: self.endResetModel())
      self._friends_reference.album_image_url_changed.connect(self._track_album_image_url_changed)

  # --- List Model Implementation ---

  def _track_album_image_url_changed(self, row: int) -> None:
    '''Tell the list model that the album image url has changed'''

    index = self.createIndex(row, 0)
    self.dataChanged.emit(index, index, [self._TRACK_IMAGE_URL])

  def roleNames(self) -> dict:
    '''Create a mapping of our enum ints to their JS object key names'''

    # Use binary strings because C++ requires it
    # TODO: Update key names to match more
    return {
      self._URL_ROLE: b'lastfmUrl',
      self._USERNAME_ROLE: b'username',
      self._REAL_NAME_ROLE: b'realName',
      self._IMAGE_URL_ROLE: b'imageUrl',
      self._TRACK_TITLE_ROLE: b'trackTitle',
      self._TRACK_ARTIST_NAME_ROLE: b'trackArtistName',
      self._TRACK_URL_ROLE: b'trackLastfmUrl',
      self._TRACK_ARTIST_URL_ROLE: b'trackArtistLastfmUrl',
      self._TRACK_IMAGE_URL: b'trackAlbumImageUrl',
      self._IS_TRACK_PLAYING_ROLE: b'isTrackPlaying',
      self._IS_TRACK_LOVED_ROLE: b'isTrackLoved',
      self._IS_LOADING_ROLE: b'isLoading'
    }

  def rowCount(self, parent: QtCore.QModelIndex=QtCore.QModelIndex()) -> int: # parent would default to None but C++ requires us to use an empty QModelIndex instead
    '''Return the number of rows in the list'''

    if self._friends_reference:
      # Prevents value from being returned if the list has a parent (is inside another list)
      if not parent.isValid():
        return len(self._friends_reference.friends)

    # Return 0 if there is no friends reference
    return 0

  def data(self, index: int, role: int=QtCore.Qt.DisplayRole) -> Union[str, bool]: # DisplayRole is a default role (object key in QML) that returns the fallback value for the data function
    if self._friends_reference:
      # Make sure the index is within the range of the row count (in the list)
      if index.isValid():
        # Get the data at the index for the ListModel to display
        friend = self._friends_reference.friends[index.row()] # index is an object with row and column methods

        # TODO: Don't use empty strings as defaults
        if role == self._URL_ROLE:
          return friend.url
        if role == self._USERNAME_ROLE:
          return friend.username
        elif role == self._REAL_NAME_ROLE:
          return friend.real_name
        elif role == self._IMAGE_URL_ROLE:
          return friend.image_url
        elif role == self._TRACK_URL_ROLE:
          return friend.last_scrobble.url if friend.last_scrobble else ''
        elif role == self._TRACK_TITLE_ROLE:
          return friend.last_scrobble.track_title if friend.last_scrobble else ''
        elif role == self._TRACK_ARTIST_NAME_ROLE:
          return friend.last_scrobble.artist_name if friend.last_scrobble else ''
        elif role == self._TRACK_ARTIST_URL_ROLE:
          return friend.last_scrobble.artist_url if friend.last_scrobble else ''
        elif role == self._TRACK_IMAGE_URL:
          return friend.last_scrobble.image_url if friend.last_scrobble else ''
        elif role == self._IS_TRACK_PLAYING_ROLE:
          return friend.last_scrobble.is_playing if friend.last_scrobble else False
        elif role == self._IS_TRACK_LOVED_ROLE:
          return friend.last_scrobble.is_loved if friend.last_scrobble else False
        elif role == self._IS_LOADING_ROLE:
          return friend.is_loading

    # This is for DisplayRole or if the friends reference doesn't exist
    return None 

  # --- Qt Properties

  friendsReference = QtCore.Property(
    type=FriendsViewModel, 
    fget=get_friends_reference, 
    fset=set_friends_reference
  )