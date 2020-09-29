from datetime import date

from PySide2 import QtCore

class FetchProfileAndTopArtistsTask(QtCore.QObject, QtCore.QRunnable):
  finished = QtCore.Signal(dict)

  def __init__(self, lastfm_instance):
    QtCore.QObject.__init__(self)
    QtCore.QRunnable.__init__(self)
    self.lastfm_instance = lastfm_instance
    self.setAutoDelete(True)

  def run(self):
    '''Fetch user account details, profile statistics, and top artists'''

    user_info = self.lastfm_instance.get_user_info()['user']
    top_artists_all_time_with_metadata = self.lastfm_instance.get_top_artists()['topartists']
    top_artists_all_time = top_artists_all_time_with_metadata['artist']
    top_artists_last_7_days = self.lastfm_instance.get_top_artists('7day')['topartists']
    total_scrobbles_today = self.lastfm_instance.get_total_scrobbles_today()

    # Calculate average daily scrobbles
    registered_timestamp = user_info['registered']['#text']
    total_days_registered = (date.today() - date.fromtimestamp(registered_timestamp)).days
    total_scrobbles = int(user_info['playcount'])
    average_daily_scrobbles = round(total_scrobbles / total_days_registered)
    
    self.finished.emit({
      'account_details': {
        'username': user_info['name'],
        'real_name': user_info['realname'],
        'lastfm_url': user_info['url'],
        'image_url': user_info['image'][-2]['#text'] # Get large size
      },
      'profile_statistics': {
        'total_scrobbles': total_scrobbles,
        'total_scrobbles_today': total_scrobbles_today,
        'average_daily_scrobbles': average_daily_scrobbles,
        'total_artists': int(top_artists_all_time_with_metadata['@attr']['total']),
        'total_loved_tracks': self.lastfm_instance.get_total_loved_tracks()
      },
      'top_artists': {
        'all_time': top_artists_all_time,
        'last_7_days': top_artists_last_7_days
      }
    })