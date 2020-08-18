class MockPlayerPlugin():
  MOCK_TRACKS = [{
    'name': 'The Way (feat. T.C.)',
    'artist': 'Hum4n01d',
    'album': 'The Way (feat. T.C.) - Single',
    'start': 0,
    'finish': 177
  }, {
    'name': 'On & On (feat. Daniel Levi)',
    'artist': 'Cartoon',
    'album': 'On & On (feat. Daniel Levi) - Single',
    'start': 0,
    'finish': 240
  }, {
    'name': 'Flames',
    'artist': 'R3HAB, ZAYN & Jungleboi',
    'album': 'Flames (The EP)',
    'start': 0,
    'finish': 221
  }, {
    'name': 'Grapevine',
    'artist': 'Tiësto',
    'album': 'Grapevine - Single',
    'start': 0,
    'finish': 221
  }, {
    'name': 'Afterlife',
    'artist': 'NCT',
    'album': 'Afterlife - Single',
    'start': 0,
    'finish': 221
  }, {
    'name': 'C**o',
    'artist': 'Jason Derulo, Puri & Jhorrmountain',
    'album': 'C**o - Single',
    'start': 0,
    'finish': 221
  }, {
    'name': 'Welcome to the Party (feat. Zhavia Ward) [From the "Deadpool 2" Original Motion Picture Soundtrack]',
    'artist': 'Diplo, French Montana & Lil Pump',
    'album': 'Welcome to the Party (feat. Zhavia Ward) [From the "Deadpool 2" Original Motion Picture Soundtrack] - Single',
    'start': 0,
    'finish': 221
  }]

  def __init__(self):
    self.has_track_loaded_variable = False
    self.current_track = {}
    self.player_position = 0
    self.next_track_index = 0

  def has_track_loaded(self):
    return self.has_track_loaded_variable

  def get_current_track(self):
    return self.current_track

  def get_next_track(self):
    track = self.MOCK_TRACKS[self.next_track_index]
    self.next_track_index += 1

    return track

  def get_player_position(self):
    return self.player_position