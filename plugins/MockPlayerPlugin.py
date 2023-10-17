from datatypes.TrackCrop import TrackCrop
import json
import os
import random
from typing import Dict

from PySide6 import QtCore
from datatypes.MediaPlayerState import MediaPlayerState

class MockPlayerPlugin(QtCore.QObject):
  # Media player signals
  stopped = QtCore.Signal()
  paused = QtCore.Signal()
  playing = QtCore.Signal(MediaPlayerState)
  cannot_scrobble_error = QtCore.Signal(str)
  showNotification = QtCore.Signal(str, str)

  MEDIA_PLAYER_NAME = 'Mock'

  # Mock player constants
  MOCK_TRACKS = json.load(open('mock_data/mock_tracks.json')) + [{
    "reason": "Test track not on Last.fm",
    "track_title": f'Fake Track {random.getrandbits(128)}',
    "artist_name": random.getrandbits(128),
    "album_title": random.getrandbits(128),
  }, {
    "reason": "Test song with no artist",
    "track_title": "localtrack.mp3"
  }] if os.environ.get('MOCK') else []

  MOCK_TRACK_LENGTH = 100

  def __init__(self):
    QtCore.QObject.__init__(self)

    self.__state: MediaPlayerState = None
    self.__track_index = 0
    self.__player_position = 0

  # --- Media Player Implementation ---

  def get_player_position(self) -> float:
    return self.__player_position

  def request_initial_state(self):
    return self.__state

  # --- Mock Specific Functions ---

  def mock_event(self, event_name):
    if event_name == 'playPause':
      if self.__state:
        if self.__state.is_playing:
          self.__state.is_playing = False
          self.paused.emit()
        else:
          self.__state.is_playing = True
          self.playing.emit(self.__state)
      else:
        self.__state = self.__get_player_state()
        self.playing.emit(self.__state)
    else:
      # Ignore other events since there's nothing playing
      if not self.__state:
        return

      if event_name == 'previous':
        self.__track_index -= 1
        self.__player_position = 0
        self.__state = self.__get_player_state()

        if self.__state.is_playing:
          self.playing.emit(self.__state)
      elif event_name == 'scrubForward':
        self.__player_position = 0.75 * MockPlayerPlugin.MOCK_TRACK_LENGTH
      elif event_name == 'next':
        self.__track_index += 1
        self.__player_position = 0
        self.__state = self.__get_player_state()

        if self.__state.is_playing:
          self.playing.emit(self.__state)

  def __get_player_state(self) -> MediaPlayerState:
    mock_track = MockPlayerPlugin.MOCK_TRACKS[self.__track_index % len(MockPlayerPlugin.MOCK_TRACKS)]

    if not mock_track.get('artist_name') or not mock_track['track_title']:
      self.cannot_scrobble_error.emit('No track title or artist name')
      return

    return MediaPlayerState(
      is_playing=self.__state.is_playing if self.__state else True,
      position=0,
      track_title=mock_track['track_title'], 
      artist_name=mock_track.get('artist_name'),
      album_title=mock_track.get('album_title'),
      album_artist_name=None,
      track_crop=TrackCrop(
        start=0,
        finish=MockPlayerPlugin.MOCK_TRACK_LENGTH
      )
    )