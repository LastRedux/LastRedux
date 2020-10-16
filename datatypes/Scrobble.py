from datetime import datetime

from datatypes.Artist import Artist
from datatypes.Album import Album
from datatypes.Track import Track

class Scrobble(Track):
  def __init__(self, track_title, artist_name, album_title=None, timestamp=None):
    '''Entry in scrobble history with track information and a timestamp'''

    # Create Track instance with associated Artist and Album instances
    super().__init__(track_title, Artist(artist_name), Album(album_title))
    
    # Automatically generate timestamp if one isn't passed
    self.timestamp = timestamp or datetime.now()