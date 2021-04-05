from PySide2 import QtCore

from ApplicationViewModel import ApplicationViewModel

class OnboardingViewModel(QtCore.QObject):
  # Qt Property signals
  has_error_changed = QtCore.Signal()
  auth_url_changed = QtCore.Signal()
  current_page_index_changed = QtCore.Signal()
  selected_media_player_changed = QtCore.Signal()

  # Signals handled by QML
  openUrl = QtCore.Signal(str)

  def __init__(self) -> None:
    QtCore.QObject.__init__(self)

    self._application_reference: ApplicationViewModel = None
    self.reset_state()

  def reset_state(self) -> None:
    # Keep track of errors, True if Last.fm can't get a session key (auth token wasn't authorized by user)
    self._has_error = None
    
    # Keep track of which onboarding page is showing
    self._current_page_index = 0

    # Store media player preference, will be written to preferences table in db
    self._selected_media_player = ''

    # Store Last.fm authorization url and auth token to share between methods
    self._auth_url = None
    self._auth_token = None

    # Store Last.fm session until we're ready to submit it to the ApplicationViewModel
    self._session = None

  # --- Qt Property Getters and Setters ---

  def set_application_reference(self, new_reference: ApplicationViewModel) -> None:
    if not new_reference:
      return

    self._application_reference = new_reference
    self._application_reference.openOnboarding.connect(self._handle_open)

  def set_has_error(self, has_error):
    self._has_error = has_error
    self.has_error_changed.emit()
  
  def set_current_page(self, page):
    self._current_page_index = page

    if page == 0: # Welcome page
      # Reset error state if you go back to the welcome page
      self.set_has_error(False)

    if page == 1: # Connecting page
      # Immediately fetch and open the authorization url
      self.openNewAuthorizationUrl()

    self.current_page_index_changed.emit()
  
  def set_selected_media_player(self, media_player_name):
    self._selected_media_player = media_player_name
    self.selected_media_player_changed.emit()
  
  # --- Slots ---

  @QtCore.Slot()
  def openNewAuthorizationUrl(self) -> None:
    '''Get an auth token, then generate and open the Last.fm user authorization url'''

    self.set_has_error(False)

    # Save the auth token for later use getting a Last.fm session
    self._auth_token = self._application_reference.lastfm.get_auth_token()

    # Save the authorization url so that it can be displayed in the UI
    self._auth_url = self._application_reference.lastfm.generate_authorization_url(self._auth_token)
    self.auth_url_changed.emit()

    # Open the authorization url by calling a QML signal that launches the user's web browser
    self.openUrl.emit(self._auth_url)
  
  @QtCore.Slot()
  def handleTryAuthenticating(self) -> None:
    '''Try getting a Last.fm session after the user authorizes the auth token in their browser'''

    try:
      # Get and store a new session from Last.fm 
      self._session = self._application_reference.lastfm.get_session(self._auth_token)
    except:
      # The auth token wasn't authorized by the user
      self._auth_url = None
      self.auth_url_changed.emit()
      self.set_has_error(True)
      return

    # Continue to choose media player page if there wasn't an error
    self.set_current_page(2)
  
  @QtCore.Slot()
  def handleFinish(self) -> None:
    '''Tell ApplicationViewModel to log in'''
    
    self._application_reference.log_in_with_onboarding_data(self._session, self._selected_media_player)

  # --- Private Methods ---

  def _handle_open(self) -> None:
    '''Reset state when onboarding opens and call signals to update UI'''

    self.reset_state()
    self.has_error_changed.emit()
    self.auth_url_changed.emit()
    self.current_page_index_changed.emit()
  
  # --- Qt Properties ---

  applicationReference = QtCore.Property(
    type=ApplicationViewModel,
    fget=lambda self: self._application_reference,
    fset=set_application_reference
  )
  
  hasError = QtCore.Property(
    type=bool, 
    fget=lambda self: self._has_error,
    fset=set_has_error,
    notify=has_error_changed
  )

  authUrl = QtCore.Property(
    type=str,
    fget=lambda self: self._auth_url,
    notify=auth_url_changed
  )

  currentPageIndex = QtCore.Property(
    type=int,
    fget=lambda self: self._current_page_index,
    fset=set_current_page,
    notify=current_page_index_changed
  )

  selectedMediaPlayer = QtCore.Property(
    type=str,
    fget=lambda self: self._selected_media_player,
    fset=set_selected_media_player,
    notify=selected_media_player_changed
  )