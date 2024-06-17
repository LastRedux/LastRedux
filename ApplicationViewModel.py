import logging

import requests
from PySide6 import QtCore, QtNetwork

from shared.components.NetworkImage import NetworkImage
from util.lastfm import LastfmApiWrapper, LastfmSession
from util.art_provider import ArtProvider
from util.spotify_api import SpotifyApiWrapper
from util import db_helper


class ApplicationViewModel(QtCore.QObject):
    # Qt Property changed signals
    is_logged_in_changed = QtCore.Signal()
    is_offline_changed = QtCore.Signal()

    # JS event signals
    openOnboarding = QtCore.Signal()
    closeOnboarding = QtCore.Signal()

    # Signals handled from QML
    isInMiniModeChanged = QtCore.Signal()
    showNotification = QtCore.Signal(str, str)

    def __init__(self) -> None:
        QtCore.QObject.__init__(self)

        # Initialize helper classes
        self.lastfm = LastfmApiWrapper()
        self.spotify_api = SpotifyApiWrapper()
        self.art_provider = ArtProvider(self.lastfm, self.spotify_api)
        self.is_logged_in = False
        self.is_offline = False

        # Store whether the app is in mini mode
        self.__is_in_mini_mode: bool = None

        # Create network request manager and expose it to all NetworkImage instances
        self.network_manager = QtNetwork.QNetworkAccessManager()
        NetworkImage.NETWORK_MANAGER = self.network_manager

        # Connect to SQLite
        db_helper.connect()

    def log_in_after_onboarding(
        self, session: LastfmSession, media_player_preference: str
    ) -> None:
        """Save new login details to db, log in, and close onboarding"""

        self.lastfm.log_in_with_session(session)

        # Save Last.fm details and app preferences to the database
        db_helper.save_lastfm_session_to_database(session)
        db_helper.save_default_preferences_to_database(media_player_preference)

        # Close onboarding and start app
        self.__set_is_logged_in(True)
        self.closeOnboarding.emit()

    def update_is_offline(self) -> None:
        try:
            requests.get("https://1.1.1.1")
            self.__set_is_offline(False)
        except requests.exceptions.ConnectionError:
            self.__set_is_offline(True)

    # --- Slots ---

    @QtCore.Slot()
    def attemptLogin(self) -> None:
        """Try to log in from database and open onboarding if they don't exist"""

        # Try to get session key and username from database
        session = db_helper.get_lastfm_session()

        if session:
            # Set Last.fm wrapper session key and username from database
            self.lastfm.log_in_with_session(session)
            self.__set_is_logged_in(True)
            logging.info(f"Logged in as {session.username}")
        else:
            self.openOnboarding.emit()

    @QtCore.Slot()
    def toggleMiniMode(self) -> None:
        self.__is_in_mini_mode = not self.__is_in_mini_mode
        self.isInMiniModeChanged.emit()
        db_helper.set_preference("is_in_mini_mode", self.__is_in_mini_mode)

    # --- Private Methods ---

    def __set_is_logged_in(self, is_logged_in: bool) -> None:
        if is_logged_in:
            # Load mini moce preference from database
            self.__is_in_mini_mode = db_helper.get_preference("is_in_mini_mode")
            self.isInMiniModeChanged.emit()

        self.is_logged_in = is_logged_in
        self.is_logged_in_changed.emit()

    def __set_is_offline(self, is_offline: bool) -> None:
        self.is_offline = is_offline
        self.is_offline_changed.emit()

    # --- Qt Properties ---

    isInMiniMode = QtCore.Property(
        type=bool, fget=lambda self: self.__is_in_mini_mode, notify=isInMiniModeChanged
    )

    isLoggedIn = QtCore.Property(
        type=bool, fget=lambda self: self.is_logged_in, notify=is_logged_in_changed
    )
