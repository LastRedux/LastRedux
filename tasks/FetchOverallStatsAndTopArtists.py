from datetime import date

from PySide2 import QtCore

from util.LastfmApiWrapper import LastfmApiWrapper
from datatypes.ListeningStatistic import ListeningStatistic
from util.helpers import listening_statistics_with_percentages

class FetchOverallAndArtistStatistics(QtCore.QObject, QtCore.QRunnable):
  finished = QtCore.Signal(dict)

  def __init__(self, lastfm_instance: LastfmApiWrapper):
    QtCore.QObject.__init__(self)
    QtCore.QRunnable.__init__(self)
    self.lastfm_instance = lastfm_instance
    self.setAutoDelete(True)

  def run(self):
    '''Fetch user account details, overall statistics, and top artists'''

    def __build_listening_statistics(lastfm_artists):
      listening_statistics = [ListeningStatistic.build_from_artist(lastfm_artist) for lastfm_artist in lastfm_artists]

      return listening_statistics_with_percentages(listening_statistics)

    # Fetch user info and overall stats
    account_details_response = self.lastfm_instance.get_account_details()
    total_scrobbles_today = self.lastfm_instance.get_total_scrobbles_today()

    # Fetch top artists
    artists_all_time_response = self.lastfm_instance.get_top_artists()
    artists_seven_days_response = self.lastfm_instance.get_top_artists('7day')

    # Calculate average daily scrobbles
    registered_timestamp = account_details_response['user']['registered']['#text']
    total_days_registered = (date.today() - date.fromtimestamp(registered_timestamp)).days
    total_scrobbles = int(account_details_response['user']['playcount'])
    average_daily_scrobbles = round(total_scrobbles / total_days_registered)

    self.finished.emit({
      'account_details': {
        'username': account_details_response['user']['name'],
        'real_name': account_details_response['user']['realname'],
        'lastfm_url': account_details_response['user']['url'],
        'image_url': account_details_response['user']['image'][-2]['#text'], # Get large size
        'large_image_url': account_details_response['user']['image'][-1]['#text'].replace('300', '500') # Get extra large size
      },
      'overall_statistics': {
        'total_scrobbles': total_scrobbles,
        'total_scrobbles_today': total_scrobbles_today,
        'average_daily_scrobbles': average_daily_scrobbles,
        'total_artists': int(artists_all_time_response['topartists']['@attr']['total']),
        'total_loved_tracks': self.lastfm_instance.get_total_loved_tracks()
      },
      'top_artists': {
        'all_time': __build_listening_statistics(artists_all_time_response['topartists']['artist']),
        'seven_days': __build_listening_statistics(artists_seven_days_response['topartists']['artist'])
      }
    })