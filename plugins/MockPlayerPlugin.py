class MockPlayerPlugin():
  MOCK_TRACKS = [{
    'title': 'Play',
    'artist_name': 'Years & Years & Jax Jones',
    'album_name': 'Palo Santo (Deluxe)',
    'start': 0,
    'finish': 221
  }, {
    'title': 'SouthSide',
    'artist_name': 'DJ Snake & Eptic',
    'album_name': 'SouthSide - Single',
    'start': 0,
    'finish': 221
  }, {
    'title': 'ON',
    'artist_name': 'BTS',
    'album_name': 'MAP OF THE SOUL : 7',
    'start': 0,
    'finish': 221
  }, {
    'title': 'Flames',
    'artist_name': 'R3HAB, ZAYN & Jungleboi',
    'album_name': 'Flames (The EP)',
    'start': 0,
    'finish': 221
  }, {
    'title': 'Flames',
    'artist_name': 'R3HAB, ZAYN & Jungleboi',
    'album_name': 'Flames (The EP)',
    'start': 0,
    'finish': 221
  }, {
    'title': 'On & On (feat. Daniel Levi)',
    'artist_name': 'Cartoon',
    'album_name': 'On & On (feat. Daniel Levi) - Single',
    'start': 0,
    'finish': 240
  }, {
    'title': 'The Way (feat. T.C.)',
    'artist_name': 'Hum4n01d',
    'album_name': 'The Way (feat. T.C.) - Single',
    'start': 0,
    'finish': 177
  }, {
    'title': 'Grapevine',
    'artist_name': 'Tiësto',
    'album_name': 'Grapevine - Single',
    'start': 0,
    'finish': 221
  }, {
    'title': 'Afterlife',
    'artist_name': 'NCT',
    'album_name': 'Afterlife - Single',
    'start': 0,
    'finish': 221
  }, {
    'title': 'C**o',
    'artist_name': 'Jason Derulo, Puri & Jhorrmountain',
    'album_name': 'C**o - Single',
    'start': 0,
    'finish': 221
  }, {
    'title': 'Welcome to the Party (feat. Zhavia Ward) [From the "Deadpool 2" Original Motion Picture Soundtrack]',
    'artist_name': 'Diplo, French Montana & Lil Pump',
    'album_name': 'Welcome to the Party (feat. Zhavia Ward) [From the "Deadpool 2" Original Motion Picture Soundtrack] - Single',
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
    track = self.MOCK_TRACKS[self.next_track_index % len(self.MOCK_TRACKS)]
    self.next_track_index += 1

    return track

  def get_player_position(self):
    return self.player_position