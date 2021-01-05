from dataclasses import dataclass

from datatypes.lastfm.LastfmScrobble import LastfmScrobble

@dataclass
class FriendTrack(LastfmScrobble):
  image_url: str
  image_url_small: str