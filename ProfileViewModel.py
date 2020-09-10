from datetime import date

from PySide2 import QtCore

import util.LastfmApiWrapper as lastfm

class ProfileViewModel(QtCore.QObject):
  user_info_changed = QtCore.Signal()
  track_listening_statistics_changed = QtCore.Signal()
  artist_listening_statistics_changed = QtCore.Signal()
  album_listening_statistics_changed = QtCore.Signal()

  def __init__(self):
    QtCore.QObject.__init__(self)

    # Get instance of lastfm api wrapper
    self.lastfm_instance = lastfm.get_static_instance()

    self.user_info = None
    self.track_listening_statistics = None
    self.artist_listening_statistics = None
    self.album_listening_statistics = None

  # --- Qt Property Getters ---

  def get_user_info(self):
    return self.user_info
  
  def get_track_listening_statistics(self):
    return self.track_listening_statistics
  
  def get_artist_listening_statistics(self):
    return self.artist_listening_statistics
  
  def get_album_listening_statistics(self):
    return self.album_listening_statistics

  # --- Slots ---
  
  @QtCore.Slot()
  def loadUserInfoAndArtistListeningStatistics(self):
    user_info = self.lastfm_instance.get_user_info()['user']
    overall_artists_info = self.lastfm_instance.get_top_artists()['topartists']
    recent_artists_info = self.lastfm_instance.get_top_artists('7day')['topartists']
    total_scrobbles_today = self.lastfm_instance.get_total_scrobbles_today()

    # Calculate average daily scrobbles
    registered_timestamp = user_info['registered']['#text']
    total_days_registered = (date.today() - date.fromtimestamp(registered_timestamp)).days
    total_scrobbles = int(user_info['playcount'])
    average_daily_scrobbles = round(total_scrobbles / total_days_registered)

    self.user_info = {
      'image_url': user_info['image'][-2]['#text'], # Get large size
      'real_name': user_info['realname'],
      'username': user_info['name'],
      'lastfm_url': user_info['url'],
      'total_scrobbles': total_scrobbles,
      'total_scrobbles_today': total_scrobbles_today,
      'average_daily_scrobbles': average_daily_scrobbles,
      'total_artists': int(overall_artists_info['@attr']['total']),
      'total_loved_tracks': self.lastfm_instance.get_total_loved_tracks()
    }

    self.artist_listening_statistics = {
      'top_artists_overall': overall_artists_info['artist'],
      'top_artists_this_week': recent_artists_info['artist']
    }

    self.user_info_changed.emit()
    self.artist_listening_statistics_changed.emit()

  @QtCore.Slot()
  def loadTrackListeningStatistics(self):
    overall_tracks_info = self.lastfm_instance.get_top_tracks()['toptracks']
    recent_tracks_info = self.lastfm_instance.get_top_tracks('7day')['toptracks']

    self.track_listening_statistics = {
      'top_tracks_overall': overall_tracks_info['track'],
      'top_tracks_this_week': recent_tracks_info['track']
    }

    self.track_listening_statistics_changed.emit()

  @QtCore.Slot()
  def loadAlbumListeningStatistics(self):
    overall_albums_info = self.lastfm_instance.get_top_albums()['topalbums']
    recent_albums_info = self.lastfm_instance.get_top_albums('7day')['topalbums']

    self.album_listening_statistics = {
      'top_albums_overall': overall_albums_info['album'],
      'top_albums_this_week': recent_albums_info['album'],
    }

    self.album_listening_statistics_changed.emit()

  # --- Qt Properties ---

  userInfo = QtCore.Property('QVariant', get_user_info, notify=user_info_changed)
  trackListeningStatistics = QtCore.Property('QVariant', get_track_listening_statistics, notify=track_listening_statistics_changed)
  artistListeningStatistics = QtCore.Property('QVariant', get_artist_listening_statistics, notify=artist_listening_statistics_changed)
  albumListeningStatistics = QtCore.Property('QVariant', get_album_listening_statistics, notify=album_listening_statistics_changed)