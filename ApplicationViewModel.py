from PySide2 import QtCore

from util.LastfmApiWrapper import LastfmApiWrapper
import util.db_helper as db_helper
from util.lastfm.LastfmSession import LastfmSession

class ApplicationViewModel(QtCore.QObject):
  # Qt Property changed signals
  is_logged_in_changed = QtCore.Signal()

  # JS event signals
  openOnboarding = QtCore.Signal()
  closeOnboarding = QtCore.Signal()

  def __init__(self):
    QtCore.QObject.__init__(self)
    
    self.lastfm: LastfmApiWrapper = LastfmApiWrapper()
    self.is_logged_in: bool = False

    # Connect to SQLite
    db_helper.connect()

  def log_in_after_onboarding(self, session: LastfmSession):
    '''Save new login details to db, log in, and close onboarding'''

    self.lastfm.log_in_with_session(session)

    # Save Last.fm details to the db
    db_helper.save_lastfm_session_to_database(session)

    # Close onboarding and start app
    self.__set_is_logged_in(True)
    self.closeOnboarding.emit()

  # --- Slots ---

  @QtCore.Slot()
  def attemptLogin(self) -> None:
    '''Try to log in from database and open onboarding if they don't exist'''

    # Try to get session key and username from database
    session = db_helper.get_lastfm_session()

    if session:
      # Set Last.fm wrapper session key and username from database
      self.lastfm.log_in_with_session(session)
      self.__set_is_logged_in(True)
    else:
      self.openOnboarding.emit()

  # --- Private Methods ---

  def __set_is_logged_in(self, is_logged_in: bool):
    self.is_logged_in = is_logged_in
    self.is_logged_in_changed.emit()

  isLoggedIn = QtCore.Property(
    type=bool, 
    fget=lambda self: self.is_logged_in, 
    fset=__set_is_logged_in, 
    notify=is_logged_in_changed
  )