from plugins.MediaPlayerPlugin import MediaPlayerPlugin

class MockPlayerPlugin(MediaPlayerPlugin):
  SONGS = [{
    'name': 'Rain On Me',
    'artist': 'Lady Gaga & Ariana Grande',
    'album': 'Rain On Me - Single',
    'start': 0,
    'finish': 182
  }, {
    'name': 'Dream Catcher',
    'artist': 'Vexento',
    'album': 'Dream Catcher - Single',
    'start': 0,
    'finish': 100
  }, {
    'name': 'Talk',
    'artist': 'Duumu',
    'album': 'Talk - Single',
    'start': 0,
    'finish': 300
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