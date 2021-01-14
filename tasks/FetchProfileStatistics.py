from dataclasses import asdict
from typing import List
from util.lastfm.LastfmAlbum import LastfmAlbum
from util.lastfm.LastfmTrack import LastfmTrack
from util.lastfm.LastfmArtist import LastfmArtist
from util.art_provider import ArtProvider
from datatypes.ProfileStatistic import ProfileStatistic
from datetime import datetime

from PySide2 import QtCore

from util.lastfm import LastfmApiWrapper
from util.spotify_api import SpotifyApiWrapper
from datatypes.ProfileStatistics import ProfileStatistics

class FetchProfileStatistics(QtCore.QObject, QtCore.QRunnable):
  finished = QtCore.Signal(ProfileStatistics)

  def __init__(self, lastfm: LastfmApiWrapper, spotify_api: SpotifyApiWrapper, art_provider: ArtProvider) -> None:
    QtCore.QObject.__init__(self)
    QtCore.QRunnable.__init__(self)
    self.lastfm = lastfm
    self.spotify_api = spotify_api
    self.art_provider = art_provider
    self.setAutoDelete(True)

  def run(self) -> None:
    '''Fetch user info, top artists and generate user statistics'''

    def __artists_to_profile_statistics(artists: List[LastfmArtist]):  
      top_plays = artists[0].plays
      
      return [
        ProfileStatistic(
          title=artist.name,
          plays=artist.plays,
          percentage=artist.plays / top_plays,
          lastfm_url=artist.url,

          # Try getting artist image from Spotify but handle a None response if not found
          image_url=getattr(self.spotify_api.get_artist(artist.name), 'image_url', None)
        ) for artist in artists
      ]

    def __tracks_to_profile_statistics(tracks: List[LastfmTrack]):  
      top_plays = tracks[0].plays
      
      return [
        ProfileStatistic(
          title=track.title,
          subtitle=track.artist.name,
          plays=track.plays,
          percentage=track.plays / top_plays,
          lastfm_url=track.url,
          secondary_lastfm_url=track.artist.url,
          image_url=self.art_provider.get_album_art(
            artist_name=track.artist.name,
            track_title=track.title
          ).small_url
        ) for track in tracks
      ]

    def __albums_to_profile_statistics(albums: List[LastfmAlbum]):  
      top_plays = albums[0].plays
      
      return [
        ProfileStatistic(
          title=album.title,
          subtitle=album.artist.name,
          plays=album.plays,
          percentage=album.plays / top_plays,
          lastfm_url=album.url,
          secondary_lastfm_url=album.artist.url,
          image_url=album.image_set.small_url or self.art_provider.get_album_art(
            artist_name=album.artist.name, 
            album_title=album.album.title
          )
        ) for album in albums
      ]

    # TODO: Make all of these requests in parallel to speed up profile page loading
    user_info = self.lastfm.get_user_info()
    top_artists = self.lastfm.get_top_artists(limit=5)

    profile_statistics = ProfileStatistics(
      total_scrobbles_today=self.lastfm.get_total_scrobbles_today(),
      total_artists=top_artists.attr_total,
      total_loved_tracks=self.lastfm.get_total_loved_tracks(),
      average_daily_scrobbles=round(
        user_info.total_scrobbles / (datetime.now() - user_info.registered_date).days
      ),
      top_artists=__artists_to_profile_statistics(top_artists.items),
      top_artists_week=__artists_to_profile_statistics(
        self.lastfm.get_top_artists(limit=5, period='7day').items
      ),
      top_albums=__albums_to_profile_statistics(
        self.lastfm.get_top_albums(limit=5)
      ),
      top_albums_week=__albums_to_profile_statistics(
        self.lastfm.get_top_albums(limit=5, period='7day')
      ),
      top_tracks=__tracks_to_profile_statistics(
        self.lastfm.get_top_tracks(limit=5)
      ),
      top_tracks_week=__tracks_to_profile_statistics(
        self.lastfm.get_top_tracks(limit=5, period='7day')
      ),
      **asdict(user_info)
    )
    
    self.finished.emit(profile_statistics)

    # def __build_listening_statistics(lastfm_artists):
    #   listening_statistics = [ListeningStatistic.build_from_artist(lastfm_artist) for lastfm_artist in lastfm_artists]

    #   return listening_statistics_with_percentages(listening_statistics)

    # # Fetch user info and overall stats
    # account_details_response = self.lastfm.get_account_details()
    # total_scrobbles_today = self.lastfm.get_total_scrobbles_today()

    # # Fetch top artists
    # artists_all_time_response = self.lastfm.get_top_artists()
    # artists_seven_days_response = self.lastfm.get_top_artists('7day')

    # # Calculate average daily scrobbles
    # registered_timestamp = account_details_response['user']['registered']['#text']
    # total_days_registered = (date.today() - date.fromtimestamp(registered_timestamp)).days
    # total_scrobbles = int(account_details_response['user']['playcount'])
    # average_daily_scrobbles = round(total_scrobbles / total_days_registered)

    # self.finished.emit({
    #   'account_details': {
    #     'username': account_details_response['user']['name'],
    #     'real_name': account_details_response['user']['realname'],
    #     'lastfm_url': account_details_response['user']['url'],
    #     'image_url': account_details_response['user']['image'][-2]['#text'], # Get large size
    #     'large_image_url': account_details_response['user']['image'][-1]['#text'].replace('300', '500') # Get extra large size
    #   },
    #   'overall_statistics': {
    #     'total_scrobbles': total_scrobbles,
    #     'total_scrobbles_today': total_scrobbles_today,
    #     'average_daily_scrobbles': average_daily_scrobbles,
    #     'total_artists': int(artists_all_time_response['topartists']['@attr']['total']),
    #     'total_loved_tracks': self.lastfm.get_total_loved_tracks()
    #   },
    #   'top_artists': {
    #     'all_time': __build_listening_statistics(artists_all_time_response['topartists']['artist']),
    #     'seven_days': __build_listening_statistics(artists_seven_days_response['topartists']['artist'])
    #   }
    # })