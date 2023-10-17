from abc import ABCMeta, abstractmethod

from PySide6 import QtCore

from datatypes.MediaPlayerState import MediaPlayerState

class MediaPlayerPlugin(QtCore.QObject):
  __metaclass__ = ABCMeta

  MEDIA_PLAYER_NAME: str
  MEDIA_PLAYER_ID: str
  IS_SUBMISSION_ENABLED: bool

  '''Emitted when the media player is not playing anything'''
  stopped = QtCore.Signal()

  '''Emitted when the media player is paused'''
  paused = QtCore.Signal()
  
  '''Emitted when the media player is playing with an updated state'''
  playing = QtCore.Signal(MediaPlayerState)

  '''Emitted when the current track can't be scrobbled or another message needs to be relayed'''
  showNotification = QtCore.Signal(str, str)

  def __init__(self) -> None:
    QtCore.QObject.__init__(self)

    # Set this to false if the plugin's dependent media player isn't installed
    self.is_available = True

  @abstractmethod
  def get_player_position(self) -> float:
    '''Get the media players current playback position in secoonds'''
    
    raise Exception('Function not implemented')

  @abstractmethod
  def is_open(self) -> bool:
    '''Return whether or not the media player is open'''
    
    raise Exception('Function not implemented')

  @abstractmethod
  def request_initial_state(self) -> MediaPlayerState:
    '''Get a MediaPlayerState object without any system notification from the media player'''

    raise Exception('Function not implemented')