import os
import json
from PySide2 import QtCore

from util.LastfmApiWrapper import LastfmApiWrapper

class FetchRecentScrobblesTask(QtCore.QObject, QtCore.QRunnable):
  finished = QtCore.Signal(list)

  def __init__(self, lastfm_instance: LastfmApiWrapper, count):
    QtCore.QObject.__init__(self)
    QtCore.QRunnable.__init__(self)
    self.lastfm_instance = lastfm_instance
    self.setAutoDelete(True)
    self.count = count

  def run(self):
    '''Return recent Last.fm scrobbles'''

    if os.environ.get('MOCK'):
      # Get the first n mock tracks in reverse order since that's how they would be added
      mock_tracks = json.load(open('mock_data/mock_tracks.json'))[0:self.count]

      mock_recent_scrobbles = []

      # Map mock track keys to Last.fm recent scrobble keys
      for i, mock_track in enumerate(mock_tracks):
        # Skip tracks with no artists (one of the mock test cases)
        if not mock_track.get('artist_name'):
          continue

        mock_recent_scrobbles.append({
          'name': mock_track['track_title'],
          'artist': {
            'name': mock_track['artist_name']
          },
          'album': {
            '#text': mock_track.get('album_title'),
          },
          'date': {
            'uts': -48899446800 + (i * 100)
          }
        })

      self.finished.emit(mock_recent_scrobbles)
    else:
      recent_scrobbles = self.lastfm_instance.get_recent_scrobbles(count=self.count)
      self.finished.emit(recent_scrobbles['recenttracks']['track'])