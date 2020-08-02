from datetime import datetime

# Entry in scrobble history with track information and a timestamp
class Scrobble:
  def __init__(self, track, artist, album, timestamp=datetime.now()):
    self.track = {
      'name': track,
      'lastfm_url': None,
      'is_loved': False,
      'plays': None,
      'tags': [],

      'album': {
        'name': album,
        'lastfm_url': None
      },

      'artist': {
        'name': artist,
        'lastfm_url': None,
        'global_listeners': None,
        'global_plays': None,
        'plays': None,
        'bio': None,
        'tags': []
      }
    }
    
    # Automatically generated
    self.timestamp = timestamp