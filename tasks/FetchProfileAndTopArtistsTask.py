from datetime import date

from PySide2 import QtCore

from datatypes.Artist import Artist

class FetchProfileAndTopArtistsTask(QtCore.QObject, QtCore.QRunnable):
  finished = QtCore.Signal(dict)

  def __init__(self, lastfm_instance):
    QtCore.QObject.__init__(self)
    QtCore.QRunnable.__init__(self)
    self.lastfm_instance = lastfm_instance
    self.setAutoDelete(True)

  def run(self):
    '''Fetch user account details, profile statistics, and top artists'''

    # Fetch user info and profile stats
    account_details = self.lastfm_instance.get_account_details()['user']
    top_artists_all_time = self.lastfm_instance.get_top_artists()
    total_scrobbles_today = self.lastfm_instance.get_total_scrobbles_today()

    # Fetch top artists
    top_artists_last_7_days = self.lastfm_instance.get_top_artists('7day')

    # Calculate average daily scrobbles
    registered_timestamp = account_details['registered']['#text']
    total_days_registered = (date.today() - date.fromtimestamp(registered_timestamp)).days
    total_scrobbles = int(account_details['playcount'])
    average_daily_scrobbles = round(total_scrobbles / total_days_registered)
    
    self.finished.emit({
      'account_details': {
        'username': account_details['name'],
        'real_name': account_details['realname'],
        'lastfm_url': account_details['url'],
        'image_url': account_details['image'][-2]['#text'] # Get large size
      },
      'profile_statistics': {
        'total_scrobbles': total_scrobbles,
        'total_scrobbles_today': total_scrobbles_today,
        'average_daily_scrobbles': average_daily_scrobbles,
        'total_artists': int(top_artists_all_time['topartists']['@attr']['total']),
        'total_loved_tracks': self.lastfm_instance.get_total_loved_tracks()
      },
      'top_artists': {
        'all_time': list(map(Artist.build_from_lastfm_artist, top_artists_all_time['topartists']['artist'])),
        'last_7_days': list(map(Artist.build_from_lastfm_artist, top_artists_last_7_days['topartists']['artist']))
      }
    })