from dataclasses import dataclass

from datatypes.Track import Track

@dataclass
class Friend:
  username: str
  real_name: str
  image_url: str
  lastfm_url: str
  is_track_playing: bool
  track: Track

  @staticmethod
  def build_from_lastfm_friend_and_recent_track(lastfm_friend, lastfm_recent_track):
    track = None
    is_track_playing = False

    # Some friends may not have any scrobbles
    if lastfm_recent_track:
      track = Track.build_from_lastfm_recent_track(lastfm_recent_track)

      if lastfm_recent_track.get('@attr', {}).get('nowplaying'):
        is_track_playing = True
    else:
      # Create an empty track object
      track = Track('', None, None)

    return Friend(
      real_name=lastfm_friend['realname'],
      username=lastfm_friend['name'],
      image_url=lastfm_friend['image'][2]['#text'], # Large size profile image
      lastfm_url=lastfm_friend['url'],
      track=track,
      is_track_playing=is_track_playing
    )