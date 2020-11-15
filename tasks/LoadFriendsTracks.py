from datetime import datetime
from typing import List

from PySide2 import QtCore

from util.LastfmApiWrapper import LastfmApiWrapper
from datatypes.Track import Track
from datatypes.Friend import Friend

class LoadFriendsTracks(QtCore.QObject, QtCore.QRunnable):
  finished = QtCore.Signal()

  def __init__(self, lastfm_instance: LastfmApiWrapper, friends: List[Friend]):
    QtCore.QObject.__init__(self)
    QtCore.QRunnable.__init__(self)
    self.lastfm_instance = lastfm_instance
    self.friends = friends
    self.setAutoDelete(True)

  def run(self):
    '''Load the passed Friend's most recent scrobble and whether or not it's playing'''

    for friend in self.friends:
      # Fetch a friend's most recent scrobble (just one)
      last_scrobble_response = self.lastfm_instance.get_recent_scrobbles(friend.username, 1)

      last_scrobble = None

      try:
        last_scrobble = last_scrobble_response['recenttracks']['track'][0]
      except IndexError:
        # There are no recent scrobbles
        friend.track = Track('', None, None)
        friend.is_track_playing = False
        continue
      
      is_currently_playing = last_scrobble.get('@attr', {}).get('nowplaying') == 'true'
      friend.is_track_playing = is_currently_playing

      # Check if scrobble was recent enough if it isn't playing
      if not is_currently_playing:
        scrobble_time = datetime.fromtimestamp(int(last_scrobble['date']['uts']))
        delta = datetime.now() - scrobble_time

        # Don't load recent scrobble if it isn't in the last 24 hours (86400 seconds) but it doesn't have to be from today
        if delta.total_seconds() >= 86400:
          friend.track = Track('', None, None)
          continue
      
      # Load track
      friend.track = Track.build_from_lastfm_recent_track(last_scrobble)

    self.finished.emit()