from dataclasses import dataclass

from datatypes.Track import Track

@dataclass
class Friend:
  username: str
  real_name: str
  image_url: str
  lastfm_url: str
  track: Track = None
  is_track_playing: bool = None
  is_loading: bool = True

  @staticmethod
  def build_from_lastfm_friend(lastfm_friend):
    '''Build a Friend from a Last.fm friend object'''
    
    return Friend(
      real_name=lastfm_friend['realname'],
      username=lastfm_friend['name'],
      image_url=lastfm_friend['image'][2]['#text'], # Large size profile image
      lastfm_url=lastfm_friend['url']
    )