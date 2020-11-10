from datatypes.MediaPlayerState import MediaPlayerState
from plugins.MediaPlayerPlugin import MediaPlayerPlugin

class MockPlayerPlugin(MediaPlayerPlugin):
  MOCK_LASTFM_TRACKS = [{
    # Test song with album on Last.fm that doesn't match Apple Music album
    'track_title': 'Don\'t Stop',
    'artist_name': 'Kuuro',
    'album_title': 'Don\'t Stop - Single',
    'track_start': 0,
    'track_finish': 100
  }, {
    # Test song with no album
    'track_title': 'Where It\'s At',
    'artist_name': 'Beck',
    'track_start': 0,
    'track_finish': 100
  }, {
    # Test song with 3 artists
    'track_title': 'Flames',
    'artist_name': 'R3HAB, ZAYN & Jungleboi',
    'album_title': 'Flames (The EP)',
    'track_start': 0,
    'track_finish': 100
  }, {
    # Test artist with diacritical marks in name
    'track_title': 'Grapevine',
    'artist_name': 'Tiësto',
    'album_title': 'Grapevine - Single',
    'track_start': 0,
    'track_finish': 221
  }, {
    # Test track with album only on Apple Music (pre-release as of 10/25/20)
    'track_title': 'NEVERMIND',
    'artist_name': 'HRVY',
    'album_title': 'Can Anybody Hear Me? (Deluxe Edition)',
    'track_start': 0,
    'track_finish': 221
  }, {
    # Test consecutive tracks with the same title
    'track_title': 'Alone',
    'artist_name': 'Marshmello',
    'album_title': 'Alone - Single',
    'track_start': 0,
    'track_finish': 100
  }, {
    # Test consecutive tracks with the same title
    'track_title': 'Alone',
    'artist_name': 'Alan Walker',
    'album_title': 'Alone - Single',
    'track_start': 0,
    'track_finish': 100
  }, {
    # Test Last.fm corrections API
    'track_title': 'Waters (feat. Phluze) [Elbor edit]',
    'artist_name': 'Elbor',
    'album_title': 'Waters (Elbor edit) [feat. Phluze] - Single',
    'track_start': 0,
    'track_finish': 100
  }, {
    # Test song with more popular remix than original on Spotify
    'track_title': 'Horsepower',
    'artist_name': 'Muzzy',
    'album_title': 'Rocket League x Monstercat, Vol. 4 - EP',
    'track_start': 0,
    'track_finish': 100
  }, {
    # Test track with censored name
    'track_title': 'C**o',
    'artist_name': 'Jason Derulo, Puri & Jhorrmountain',
    'album_title': 'C**o - Single',
    'track_start': 0,
    'track_finish': 221
  }, {
    # Test track from soundtrack album
    'track_title': 'Welcome to the Party (feat. Zhavia Ward) [From the "Deadpool 2" Original Motion Picture Soundtrack]',
    'artist_name': 'Diplo, French Montana & Lil Pump',
    'album_title': 'Welcome to the Party (feat. Zhavia Ward) [From the "Deadpool 2" Original Motion Picture Soundtrack] - Single',
    'track_start': 0,
    'track_finish': 221
  }, {
    # Test song with no Spotify results (artist names don't match between platforms)
    'track_title': 'Shut It Down (feat. MC Mota)',
    'artist_name': 'Muzzy & Teddy Killers',
    'album_title': 'The Cascade - EP',
    'track_start': 0,
    'track_finish': 100
  }, {
    # Test track with super long list of artists
    'track_title': 'Interstate 5 (feat. Azure Onyxscore, Hum4n01d, Arimyth, Mr. Serpent, console.frog, SpaghettiSauce, INDIR3CT & Glacial Viper)',
    'artist_name': 'Auxy Collective',
    'album_title': 'Interstate 5 (feat. Azure Onyxscore, Hum4n01d, Arimyth, Mr. Serpent, console.frog, SpaghettiSauce, INDIR3CT & Glacial Viper) - Single',
    'track_start': 0,
    'track_finish': 221
  }]

  # Add tracks that aren't on Last.fm to test media player edge cases
  MOCK_TRACKS = MOCK_LASTFM_TRACKS + [{
    # Test track not on Last.fm
    'track_title': 'Wodd! Dow!',
    'artist_name': 'chipadip',
    'album_title': 'dowwd: the comp',
    'track_start': 0,
    'track_finish': 221
  }, {
    # Test song with no artist
    'track_title': 'localtrack.mp3',
    'track_start': 0,
    'track_finish': 100
  }]

  def __init__(self):
    self.current_track = {}
    self.track_index = 13
    self.player_position = 0

  def get_state(self):
    if self.track_index != -1:
      track = self.MOCK_TRACKS[self.track_index % len(self.MOCK_TRACKS)]

      return MediaPlayerState(True, self.player_position, **track)
    
    return MediaPlayerState()
