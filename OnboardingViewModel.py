from PySide2 import QtCore, QtSql

from ApplicationViewModel import ApplicationViewModel

import util.LastfmApiWrapper as lastfm

class OnboardingViewModel(QtCore.QObject):
  has_error_changed = QtCore.Signal()
  auth_url_changed = QtCore.Signal()
  current_page_changed = QtCore.Signal()
  openUrl = QtCore.Signal(str)

  def initialize_variables(self):
    self.__has_error = None
    self.__current_page = 0
    self.__auth_url = None
    self.__auth_token = None
    self.__temporary_session_key = None
    self.__temporary_username = None
  
  def __init__(self):
    QtCore.QObject.__init__(self)

    self.initialize_variables()
    self.__application = None
    self.__lastfm_instance = lastfm.get_static_instance()

  def __handle_open(self):
    self.initialize_variables()
    self.has_error_changed.emit()
    self.auth_url_changed.emit()
    self.current_page_changed.emit()

  def set_application_reference(self, new_reference):
    if new_reference:
      self.__application_reference = new_reference
      self.__application_reference.openOnboarding.connect(self.__handle_open)

  def set_has_error(self, has_error):
    self.__has_error = has_error
    self.has_error_changed.emit()
  
  def set_current_page(self, page):
    self.__current_page = page

    if page == 0:
      self.set_has_error(False)

    if page == 1: # Connecting page
      self.openNewAuthorizationUrl()

    self.current_page_changed.emit()
  
  @QtCore.Slot()
  def openNewAuthorizationUrl(self):
    self.set_has_error(False)
    self.__auth_token = self.__lastfm_instance.get_auth_token()
    self.__auth_url = self.__lastfm_instance.generate_authorization_url(self.__auth_token)
    self.openUrl.emit(self.__auth_url)
    self.auth_url_changed.emit()
  
  @QtCore.Slot()
  def authenticate(self):
    if self.__auth_token:
      # Get and save a new session key from Last.fm 
      try:
        self.__temporary_session_key, self.__temporary_username = self.__lastfm_instance.get_session_key_and_username(self.__auth_token)
        self.set_current_page(2)
      except Exception:
        self.__auth_url = None
        self.auth_url_changed.emit()
        self.set_has_error(True)
  
  @QtCore.Slot()
  def finish(self):
    if self.__application_reference:
      self.__application_reference.log_in(self.__temporary_session_key, self.__temporary_username)
  
  applicationReference = QtCore.Property(ApplicationViewModel, lambda self: self.__application_reference, set_application_reference)
  hasError = QtCore.Property(bool, lambda self: self.__has_error, set_has_error, notify=has_error_changed)
  authUrl = QtCore.Property(str, lambda self: self.__auth_url, notify=auth_url_changed)
  currentPage = QtCore.Property(int, lambda self: self.__current_page, set_current_page, notify=current_page_changed)