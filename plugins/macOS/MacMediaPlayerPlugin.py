from abc import ABCMeta, abstractmethod

from plugins.MediaPlayerPlugin import MediaPlayerPlugin

class MacMediaPlayerPlugin(MediaPlayerPlugin):
  __metaclass__ = ABCMeta

  # Constants from BridgeSupport enum definitions used by the Music.app and Spotify AppleScript APIs
  PLAYING_STATE = 1800426320
  STOPPED_STATE = 1800426323
  PAUSED_STATE = 1800426352

  def __init__(self, applescript_app) -> None:
    super().__init__()

    self.__applescript_app = applescript_app

  # --- Media Player Implementation ---

  def get_player_position(self) -> float:
    return self.__applescript_app.playerPosition()

  def is_open(self) -> bool:
    return self.__applescript_app.isRunning()

  @abstractmethod
  def request_initial_state(self) -> None:
    '''Get a MediaPlayerState object without any system notification from the media player'''

    pass