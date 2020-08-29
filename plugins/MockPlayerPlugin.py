from datatypes.MediaPlayerState import MediaPlayerState

class MockPlayerPlugin():
  MOCK_TRACKS = [{
    'track_title': 'Glitter',
    'artist_name': 'BENEE',
    'album_title': 'Fire on Marzz - EP',
    'track_start': 0,
    'track_finish': 221
  }, {
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
    'track_title': 'ON',
    'artist_name': 'BTS',
    'album_title': 'MAP OF THE SOUL : 7',
    'track_start': 0,
    'track_finish': 221
  }, {
    'track_title': 'Flames',
    'artist_name': 'R3HAB, ZAYN & Jungleboi',
    'album_title': 'Flames (The EP)',
    'track_start': 0,
    'track_finish': 221
  }, {
    'track_title': 'On & On (feat. Daniel Levi)',
    'artist_name': 'Cartoon',
    'album_title': 'On & On (feat. Daniel Levi) - Single',
    'track_start': 0,
    'track_finish': 240
  }, {
    'track_title': 'The Way (feat. T.C.)',
    'artist_name': 'Hum4n01d',
    'album_title': 'The Way (feat. T.C.) - Single',
    'track_start': 0,
    'track_finish': 177
  }, {
    'track_title': 'Grapevine',
    'artist_name': 'Tiësto',
    'album_title': 'Grapevine - Single',
    'track_start': 0,
    'track_finish': 221
  }, {
    'track_title': 'Afterlife',
    'artist_name': 'NCT',
    'album_title': 'Afterlife - Single',
    'track_start': 0,
    'track_finish': 221
  }, {
    'track_title': 'C**o',
    'artist_name': 'Jason Derulo, Puri & Jhorrmountain',
    'album_title': 'C**o - Single',
    'track_start': 0,
    'track_finish': 221
  }, {
    'track_title': 'Welcome to the Party (feat. Zhavia Ward) [From the "Deadpool 2" Original Motion Picture Soundtrack]',
    'artist_name': 'Diplo, French Montana & Lil Pump',
    'album_title': 'Welcome to the Party (feat. Zhavia Ward) [From the "Deadpool 2" Original Motion Picture Soundtrack] - Single',
    'track_start': 0,
    'track_finish': 221
  }]

  def __init__(self):
    self.has_track_loaded_variable = False
    self.current_track = {}
    self.__next_track_index = -1
    self.player_position = 0

  def get_next_track(self):
    track = self.MOCK_TRACKS[self.__next_track_index % len(self.MOCK_TRACKS)]
    self.__next_track_index += 1

  def get_state(self):
    if self.__next_track_index != -1:
      track = self.MOCK_TRACKS[self.__next_track_index % len(self.MOCK_TRACKS)]

      return MediaPlayerState(True, self.player_position, **track)
    
    return MediaPlayerState()
