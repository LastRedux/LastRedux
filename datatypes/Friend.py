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
  
  # # WIP CODE for comparing friends - not working
  # # TODO: Look into why "Friend" type annotation doesn't work here, it works in Track
  # def equals(self, other_friend):
  #   '''Compare two friends'''
    
  #   if not other_friend:
  #     return False
    
  #   tracks_equal = None

  #   if self.track is None or other_friend.track is None:
  #     tracks_equal = False
  #   else:
  #     tracks_equal = self.track.equals(other_friend.track)

  #   return (
  #     self.username == other_friend.username
  #     and self.real_name == other_friend.real_name
  #     and self.image_url == other_friend.image_url
  #     and tracks_equal
  #     and self.is_track_playing == other_friend.is_track_playing
  #     and self.is_loading == other_friend.is_loading
  #   )