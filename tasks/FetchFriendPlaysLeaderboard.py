from PySide2 import QtCore

from util.lastfm import LastfmApiWrapper, LastfmArtist, LastfmTrack, LastfmUser
from datatypes import ProfileStatistic

class FetchFriendPlaysLeaderboard(QtCore.QObject, QtCore.QRunnable):
  finished = QtCore.Signal(list, list)

  def __init__(self, lastfm: LastfmApiWrapper, track: LastfmTrack):
    QtCore.QObject.__init__(self)
    QtCore.QRunnable.__init__(self)
    self.lastfm = lastfm
    self.track = track
    self.setAutoDelete(True)

  def run(self):
    '''Fetch play statistics for the user's Last.fm friends'''

    def __generate_statistic(user: LastfmUser, plays: int) -> ProfileStatistic:
      return ProfileStatistic(
        title=user.username,
        plays=plays,
        image_url=user.image_url,
        lastfm_url=user.url
      )
    
    friends = self.lastfm.get_friends()
    artist_leaderboard = []
    track_leaderboard = []

    # Add logged in user to friends to list in the leaderboard
    # TODO: Request cached data
    friends.append(self.lastfm.get_user_info())

    for user in friends:
      artist_info = self.lastfm.get_artist_info(self.track.artist.name, user.username)
      track_info = self.lastfm.get_track_info(self.track.artist.name, self.track.title, user.username)

      if artist_info.plays:
        artist_leaderboard.append(__generate_statistic(user, artist_info.plays))
      
      if track_info.plays:
        track_leaderboard.append(__generate_statistic(user, track_info.plays))

    artist_leaderboard = sorted(artist_leaderboard, key=lambda stat: stat.plays, reverse=True)
    track_leaderboard = sorted(track_leaderboard, key=lambda stat: stat.plays, reverse=True)

    return artist_leaderboard, track_leaderboard