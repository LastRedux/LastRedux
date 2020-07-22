from PySide2 import QtCore

from ApplicationViewModel import *

class ScrobbleDetailsViewModel(QtCore.QObject):
  scrobble_changed = QtCore.Signal()

  def __init__(self):
    QtCore.QObject.__init__(self)
    self.__application = None
  
  def application_selected_scrobble_changed(self):
    # TODO: Load scrobble data from Last.fm API
    self.scrobble_changed.emit()

  def get_application(self):
    return self.__application

  def set_application(self, new_application):
    if new_application:
      self.__application = new_application
      self.__application.selected_scrobble_changed.connect(self.application_selected_scrobble_changed)
      self.scrobble_changed.emit()
  
  # Selected scrobble
  def get_track(self):
    if self.__application:
      if self.__application.selected_scrobble:
        return self.__application.selected_scrobble.track
    
    return ''
  
  def get_artist(self):
    if self.__application:
      if self.__application.selected_scrobble:
        return self.__application.selected_scrobble.artist
    
    return ''
  
  def get_album(self):
    if self.__application:
      if self.__application.selected_scrobble:
        return self.__application.selected_scrobble.album
    
    return ''
  
  # Properties
  application = QtCore.Property(ApplicationViewModel, get_application, set_application)
  track = QtCore.Property(str, get_track, notify=scrobble_changed)
  artist = QtCore.Property(str, get_artist, notify=scrobble_changed)
  album = QtCore.Property(str, get_album, notify=scrobble_changed)