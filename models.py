from datetime import datetime

class Scrobble:
  def __init__(self, track, artist, album, timestamp=datetime.now()):
    '''Entry in scrobble history with track information and a timestamp'''

    self.track = {
      'is_additional_data_downloaded': False,
      'name': track,
      'lastfm_url': None,
      'is_loved': False,
      'plays': None,
      'tags': [],

      'album': {
        'name': album,
        'lastfm_url': None,
        'plays': None,
        'image_url': None,
        'image_url_small': None
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