import json
import random
from typing import Dict

from PySide2 import QtCore
from datatypes.MediaPlayerState import MediaPlayerState

class MockPlayerPlugin(QtCore.QObject):
  # Media player signals
  stopped = QtCore.Signal()
  paused = QtCore.Signal(MediaPlayerState)
  playing = QtCore.Signal(MediaPlayerState)

  # Mock player constants
  MOCK_TRACKS = json.load(open('mock_data/mock_tracks.json')) + [{
    "reason": "Test track not on Last.fm",
    "track_title": f'Fake Track {random.getrandbits(128)}',
    "artist_name": random.getrandbits(128),
    "album_title": random.getrandbits(128),
  }, {
    "reason": "Test song with no artist",
    "track_title": "localtrack.mp3",

  }]
  MOCK_TRACK_LENGTH = 100

  def __init__(self):
    QtCore.QObject.__init__(self)

    self.__state: MediaPlayerState = None
    self.__track_index = 0
    self.__player_position = 0

  # --- Media Player Implementation ---

  def get_player_position(self) -> float:
    return self.__player_position

  # --- Mock Specific Functions ---

  def mock_event(self, event_name):
    if not self.__state:
      if event_name == 'playPause':
        # Load first track
        self.__update_state()
        self.playing.emit(self.__state)

      # Ignore other events since nothing is playing
      return

    if event_name == 'previous':
      self.__track_index -= 1
      self.__player_position = 0
      self.__update_state()
      self.playing.emit(self.__state)
    elif event_name == 'playPause':
      if self.__state.is_playing:
        self.paused.emit(self.__state)
      else:
        self.playing.emit(self.__state)
      
      self.__state.is_playing = not self.__state.is_playing
    elif event_name == 'scrubForward':
      self.__player_position = 0.75 * MockPlayerPlugin.MOCK_TRACK_LENGTH
    elif event_name == 'next':
      self.__track_index += 1
      self.__player_position = 0
      self.__update_state()
      self.playing.emit(self.__state)

  def __update_state(self):
    mock_track = MockPlayerPlugin.MOCK_TRACKS[self.__track_index % len(MockPlayerPlugin.MOCK_TRACKS)]

    self.__state = MediaPlayerState(
      is_playing=True, 
      track_title=mock_track['track_title'], 
      artist_name=mock_track.get('artist_name'),
      album_title=mock_track.get('album_title'), 
      track_start=0,
      track_finish=MockPlayerPlugin.MOCK_TRACK_LENGTH
    )
