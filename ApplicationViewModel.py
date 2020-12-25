from PySide2 import QtCore

import util.db_helper as db_helper
import util.LastfmApiWrapper as lastfm

class ApplicationViewModel(QtCore.QObject):
  # Qt Property changed signals
  is_logged_in_changed = QtCore.Signal()

  # JS event signals
  openOnboarding = QtCore.Signal()
  closeOnboarding = QtCore.Signal()

  def __init__(self):
    QtCore.QObject.__init__(self)
    self.is_logged_in = False

    # Get instance of lastfm api wrapper
    self.lastfm_instance = lastfm.get_static_instance()

    # Connect to SQLite
    db_helper.connect()

  def log_in(self, session_key, username):
    self.lastfm_instance.set_login_info(session_key, username)
    db_helper.create_lastfm_session_details(session_key, username)
    self.set_is_logged_in(True)
    self.closeOnboarding.emit()

  def set_is_logged_in(self, is_logged_in):
    self.is_logged_in = is_logged_in
    self.is_logged_in_changed.emit()

  @QtCore.Slot()
  def attemptLogin(self):
    db_helper.get_lastfm_session_details()

    # Try to get session key and username from database
    session_key, username = db_helper.get_lastfm_session_details()

    if session_key:
      # Set Last.fm wrapper session key and username from database
      self.lastfm_instance.set_login_info(session_key, username)
      self.set_is_logged_in(True)
    else:
      self.openOnboarding.emit()

  isLoggedIn = QtCore.Property(bool, lambda self: self.is_logged_in, set_is_logged_in, notify=is_logged_in_changed)