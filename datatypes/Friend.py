from dataclasses import dataclass

from datatypes.Track import Track

@dataclass
class Friend:
  username: str
  real_name: str
  image_url: str
  lastfm_url: str
  current_track: Track
  is_current_track_playing: bool

  @staticmethod
  def build_from_lastfm_friend_and_recent_track(lastfm_friend, lastfm_recent_track):
    return Friend(
      real_name=lastfm_friend['realname'],
      username=lastfm_friend['name'],
      image_url=lastfm_friend['image'][2]['#text'], # Large size profile image
      lastfm_url=lastfm_friend['url'],
      current_track=Track.build_from_lastfm_recent_track(lastfm_recent_track),
      is_current_track_playing=lastfm_recent_track.get('@attr', {}).get('nowplaying') or False
    )