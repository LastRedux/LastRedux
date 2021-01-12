from dataclasses import asdict, dataclass
from datatypes.ProfileStatistic import ProfileStatistic

from util.lastfm.LastfmUserInfo import LastfmUserInfo

@dataclass
class ProfileStatistics(LastfmUserInfo):
  total_scrobbles_today: int
  average_daily_scrobbles: int
  total_artists: int
  total_loved_tracks: int
  
  # Top artists
  top_artists: ProfileStatistic
  top_artists_week: ProfileStatistic
  
  # Top albums
  top_albums: ProfileStatistic
  top_albums_week: ProfileStatistic

  # Top tracks
  top_tracks: ProfileStatistic
  top_tracks_week: ProfileStatistic