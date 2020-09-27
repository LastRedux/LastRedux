from PySide2 import QtCore

from FriendsViewModel import FriendsViewModel

class FriendsListModel(QtCore.QAbstractListModel):
  __USERNAME_ROLE = QtCore.Qt.UserRole
  __REAL_NAME_ROLE = QtCore.Qt.UserRole + 1
  __IMAGE_URL_ROLE = QtCore.Qt.UserRole + 2
  __LASTFM_URL_ROLE = QtCore.Qt.UserRole + 3
  __CURRENT_TRACK_TITLE_ROLE = QtCore.Qt.UserRole + 4
  __CURRENT_TRACK_ARTIST_NAME_ROLE = QtCore.Qt.UserRole + 5
  __CURRENT_TRACK_IS_PLAYING_ROLE = QtCore.Qt.UserRole + 6
  __CURRENT_TRACK_LASTFM_URL_ROLE = QtCore.Qt.UserRole + 7

  def __int__(self, parent=None):
    QtCore.QAbstractListModel.__init__(self, parent)

    self.__friends_reference = None

  # --- Qt Property Getters and Setters ---

  def get_friends_reference(self):
    return self.__friends_reference

  def set_friends_reference(self, newReference):
    if newReference:
      self.beginResetModel()
      self.__friends_reference = newReference
      self.endResetModel()

      self.__friends_reference.begin_refresh_friends.connect(lambda: self.beginResetModel())
      self.__friends_reference.end_refresh_friends.connect(lambda: self.endResetModel())

  # --- List Model Implementation ---

  def roleNames(self):
    '''Create a mapping of our enum ints to their JS object key names'''

    # Use binary strings because C++ requires it
    return {
      self.__USERNAME_ROLE: b'username',
      self.__REAL_NAME_ROLE: b'realName',
      self.__IMAGE_URL_ROLE: b'imageUrl',
      self.__LASTFM_URL_ROLE: b'lastfmUrl',
      self.__CURRENT_TRACK_TITLE_ROLE: b'currentTrackTitle',
      self.__CURRENT_TRACK_ARTIST_NAME_ROLE: b'currentTrackArtistName',
      self.__CURRENT_TRACK_IS_PLAYING_ROLE: b'currentTrackIsPlaying',
      self.__CURRENT_TRACK_LASTFM_URL_ROLE: b'currentTrackLastfmUrl'
    }

  def rowCount(self, parent=QtCore.QModelIndex()):
    '''Return the number of rows in the list''' 

    if self.__friends_reference:
      # Prevents value from being returned if the list has a parent (is inside another list)
      if not parent.isValid():
        return len(self.__friends_reference.friends)

    # Return 0 if there is no friends reference
    return 0

  def data(self, index, role=QtCore.Qt.DisplayRole): # DisplayRole is a default role (object key in QML) that returns the fallback value for the data function
    if self.__friends_reference:
      # Make sure the index is within the range of the row count (in the list)
      if index.isValid():
        # Get the data at the index for the ListModel to display
        friend = self.__friends_reference.friends[index.row()] # index is an object with row and column methods

        if role == self.__USERNAME_ROLE:
          return friend.username
        elif role == self.__REAL_NAME_ROLE:
          return friend.real_name
        elif role == self.__IMAGE_URL_ROLE:
          return friend.image_url
        elif role == self.__LASTFM_URL_ROLE:
          return friend.lastfm_url
        elif role == self.__CURRENT_TRACK_TITLE_ROLE:
          return friend.current_track.title
        elif role == self.__CURRENT_TRACK_ARTIST_NAME_ROLE:
          return friend.current_track.artist.name
        elif role == self.__CURRENT_TRACK_LASTFM_URL_ROLE:
          return friend.current_track.lastfm_url
        elif role == self.__CURRENT_TRACK_IS_PLAYING_ROLE:
          return friend.is_current_track_playing

    # This is for DisplayRole or if the friends reference doesn't exist
    return None 

  friendsReference = QtCore.Property(FriendsViewModel, get_friends_reference, set_friends_reference)