from PySide2 import QtCore

from util.helpers import listening_statistics_with_percentages
from util.LastfmApiWrapper import LastfmApiWrapper
from datatypes.ListeningStatistic import ListeningStatistic

class FetchTopAlbumsTask(QtCore.QObject, QtCore.QRunnable):
  finished = QtCore.Signal(dict)

  def __init__(self, lastfm_instance: LastfmApiWrapper):
    QtCore.QObject.__init__(self)
    QtCore.QRunnable.__init__(self)
    self.lastfm_instance = lastfm_instance
    self.setAutoDelete(True)

  def run(self):
    '''Fetch a user's top albums from Last.fm'''

    def __build_listening_statistics(lastfm_albums):
      listening_statistics = [ListeningStatistic.build_from_album(lastfm_album) for lastfm_album in lastfm_albums]

      return listening_statistics_with_percentages(listening_statistics)

    all_time_response = self.lastfm_instance.get_top_albums()
    seven_days_response = self.lastfm_instance.get_top_albums('7day')

    self.finished.emit({
      'all_time': __build_listening_statistics(all_time_response['topalbums']['album']),
      'seven_days': __build_listening_statistics(seven_days_response['topalbums']['album'])
    })