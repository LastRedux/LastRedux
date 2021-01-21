from abc import ABCMeta, abstractmethod

from PySide2 import QtCore

from datatypes.MediaPlayerState import MediaPlayerState

class MediaPlayerPlugin(QtCore.QObject):
  __metaclass__ = ABCMeta

  MEDIA_PLAYER_NAME: str = None
  MEDIA_PLAYER_ID: str = None
  IS_SUBMISSION_ENABLED: bool = None

  '''Emitted when the media player is not playing anything'''
  stopped = QtCore.Signal()

  '''Emitted when the media player is paused with an updated state'''
  paused = QtCore.Signal(MediaPlayerState)
  
  '''Emitted when the media player is playing with an updated state'''
  playing = QtCore.Signal(MediaPlayerState)

  '''Emitted when the current track can't be scrobbled'''
  cannot_scrobble_error = QtCore.Signal(str)

  def __init__(self) -> None:
    QtCore.QObject.__init__(self)

    # Set this to false if the plugin's dependent media player isn't installed
    self.is_available = True

  @abstractmethod
  def get_player_position(self) -> float:
    '''Get the media players current playback position in secoonds'''
    
    pass

  @abstractmethod
  def is_open(self) -> bool:
    '''Return whether or not the media player is open'''
    
    pass

  @abstractmethod
  def request_initial_state(self) -> None:
    '''Get a MediaPlayerState object without any system notification from the media player'''

    pass