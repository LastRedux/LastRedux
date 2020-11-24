import Foundation
import ctypes
import objc
from PySide2 import QtCore

class MacNotificationObserver(QtCore.QObject):
  def __init__(self) -> None:
    QtCore.QObject.__init__(self)
    objc.setVerbose(1)

  def handleNotificationFromMusic_(self, notification):
    user_info = notification.userInfo()
    player_state = user_info['Player State']

    if player_state == 'Stopped':
      print('Music stopped')

      return

    track_title = user_info['Name']

    if track_title == 'Connecting…':
      print('Connecting')
      return
      
    artist_name = user_info['Artist']
    album_title = user_info['Album']

    print(f'Now {player_state}: {artist_name} - {track_title} | {album_title}')

  @QtCore.Slot()
  def makeConnections(self) -> None:
    # Using https://lethain.com/how-to-use-selectors-in-pyobjc/ as reference
    # selector = objc.selector(self.handleNotificationFromMusic_notifcation_)
    default_center = Foundation.NSDistributedNotificationCenter.defaultCenter()
    observer = default_center.addObserver_selector_name_object_(self, 'handleNotificationFromMusic:', 'com.apple.iTunes.playerInfo', None)#'com.apple.Music.player')

    print(default_center)
    print('ok')