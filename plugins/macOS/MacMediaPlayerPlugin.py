from abc import ABCMeta, abstractmethod

from plugins.MediaPlayerPlugin import MediaPlayerPlugin

class MacMediaPlayerPlugin(MediaPlayerPlugin):
  __metaclass__ = ABCMeta

  # Constants
  PLAYING_STATE = 1800426320 # From BridgeSupport enum definitions, used by Music.app and Spotify

  def __init__(self, applescript_app) -> None:
    super().__init__()

    self.__applescript_app = applescript_app

  # --- Media Player Implementation ---

  def get_player_position(self) -> float:
    return self.__applescript_app.playerPosition()

  def is_open(self) -> bool:
    return self.__applescript_app.isRunning()

  @abstractmethod
  def force_initial_notification(self) -> None:
    '''Get a MediaPlayerState object without any system notification from the media player'''

    pass