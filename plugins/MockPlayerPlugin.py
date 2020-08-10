from plugins.MediaPlayerPlugin import MediaPlayerPlugin

class MockPlayerPlugin():
  SONGS = [{
    'name': 'Rain On Me',
    'artist': 'Lady Gaga & Ariana Grande',
    'album': 'Chromatica',
    'start': 0,
    'finish': 240
  }, {
    'name': 'Girlfriend',
    'artist': 'Charlie Puth',
    'album': 'Girlfriend - Single',
    'start': 0,
    'finish': 177
  }, {
    'name': 'Funny',
    'artist': 'Zedd & Jasmine Thompson',
    'album': 'Funny - Single',
    'start': 0,
    'finish': 221
  }]

  def __init__(self):
    self.has_track_loaded_variable = False
    self.current_track = {}
    self.player_position = 0

  def has_track_loaded(self):
    return self.has_track_loaded_variable

  def get_current_track(self):
    return self.current_track

  def get_player_position(self):
    return self.player_position