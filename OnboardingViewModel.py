from PySide2 import QtCore

from ApplicationViewModel import ApplicationViewModel

class OnboardingViewModel(QtCore.QObject):
  # Qt Property signals
  has_error_changed = QtCore.Signal()
  auth_url_changed = QtCore.Signal()
  current_page_index_changed = QtCore.Signal()

  # Signals handled by QML
  openUrl = QtCore.Signal(str)

  def __init__(self):
    QtCore.QObject.__init__(self)

    self.__application_reference: ApplicationViewModel = None
    self.reset_state()

  def reset_state(self):
    # Keep track of errors, True if Last.fm can't get a session key (auth token wasn't authorized by user)
    self.__has_error = None
    
    # Keep track of which onboarding page is showing
    self.__current_page_index = 0

    # Store Last.fm authorization url and auth token to share between methods
    self.__auth_url = None
    self.__auth_token = None

    # Store Last.fm session until we're ready to submit it to the ApplicationViewModel
    self.__session = None

  # --- Qt Property Getters and Setters ---

  def set_application_reference(self, new_reference):
    if new_reference:
      self.__application_reference = new_reference
      self.__application_reference.openOnboarding.connect(self.__handle_open)

  def set_has_error(self, has_error):
    self.__has_error = has_error
    self.has_error_changed.emit()
  
  def set_current_page(self, page):
    self.__current_page_index = page

    if page == 0: # Welcome page
      # Reset error state if you go back to the welcome page
      self.set_has_error(False)

    if page == 1: # Connecting page
      # Immediately fetch and open the authorization url
      self.openNewAuthorizationUrl()

    self.current_page_index_changed.emit()
  
  # --- Slots ---

  @QtCore.Slot()
  def openNewAuthorizationUrl(self):
    '''Get an auth token, then generate and open the Last.fm user authorization url'''

    self.set_has_error(False)

    # Save the auth token for later use getting a Last.fm session
    self.__auth_token = self.__application_reference.lastfm.get_auth_token()

    # Save the authorization url so that it can be displayed in the UI
    self.__auth_url = self.__application_reference.lastfm.generate_authorization_url(self.__auth_token)
    self.auth_url_changed.emit()

    # Open the authorization url by calling a QML signal that launches the user's web browser
    self.openUrl.emit(self.__auth_url)
  
  @QtCore.Slot()
  def handleTryAuthenticating(self):
    '''Try getting a Last.fm session after the user authorizes the auth token in their browser'''

    try:
      # Get and store a new session from Last.fm 
      self.__session = self.__application_reference.lastfm.get_session(self.__auth_token)
    except:
      # The auth token wasn't authorized by the user
      self.__auth_url = None
      self.auth_url_changed.emit()
      self.set_has_error(True)
      return

    # Continue to finished page if there wasn't an error
    self.set_current_page(2)
  
  @QtCore.Slot()
  def handleFinish(self):
    '''Tell ApplicationViewModel to log in'''
    
    self.__application_reference.log_in_after_onboarding(self.__session)

  # --- Private Methods ---

  def __handle_open(self):
    '''Reset state when onboarding opens and call signals to update UI'''

    self.reset_state()
    self.has_error_changed.emit()
    self.auth_url_changed.emit()
    self.current_page_index_changed.emit()
  
  # --- Qt Properties ---

  applicationReference = QtCore.Property(
    type=ApplicationViewModel,
    fget=lambda self: self.__application_reference,
    fset=set_application_reference
  )
  
  hasError = QtCore.Property(
    type=bool, 
    fget=lambda self: self.__has_error,
    fset=set_has_error,
    notify=has_error_changed
  )

  authUrl = QtCore.Property(
    type=str,
    fget=lambda self: self.__auth_url,
    notify=auth_url_changed
  )

  currentPageIndex = QtCore.Property(
    type=int,
    fget=lambda self: self.__current_page_index,
    fset=set_current_page,
    notify=current_page_index_changed
  )