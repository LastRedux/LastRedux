from PySide2 import QtCore

from util.helpers import listening_statistics_with_percentages
from util.LastfmApiWrapper import LastfmApiWrapper
from datatypes.ListeningStatistic import ListeningStatistic

class FetchTopTracksTask(QtCore.QObject, QtCore.QRunnable):
  finished = QtCore.Signal(dict)

  def __init__(self, lastfm_instance: LastfmApiWrapper):
    QtCore.QObject.__init__(self)
    QtCore.QRunnable.__init__(self)
    self.lastfm_instance = lastfm_instance
    self.setAutoDelete(True)

  def run(self):
    '''Fetch a user's top tracks from Last.fm'''

    def __build_listening_statistics(lastfm_tracks):
      listening_statistics = [ListeningStatistic.build_from_track(lastfm_track) for lastfm_track in lastfm_tracks]

      return listening_statistics_with_percentages(listening_statistics)

    all_time_track_response = self.lastfm_instance.get_top_tracks()
    seven_days_track_response = self.lastfm_instance.get_top_tracks('7day')

    self.finished.emit({
      'all_time': __build_listening_statistics(all_time_track_response['toptracks']['track']),
      'seven_days': __build_listening_statistics(seven_days_track_response['toptracks']['track'])
    })