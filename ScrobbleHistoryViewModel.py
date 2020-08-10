import os
from threading import Thread

from PySide2 import QtCore, QtSql

from plugins.MockPlayerPlugin import MockPlayerPlugin
from plugins.AppleMusicPlugin import AppleMusicPlugin
from LastFmApiWrapper import LastFmApiWrapper
from models import Scrobble

class MediaPlayerThreadWorker(QtCore.QObject):
  # TODO: Use Python threads instead of QThreads
  
  finished_getting_media_player_data = QtCore.Signal()

  def __init__(self):
    QtCore.QObject.__init__(self)
    self.scrobble_history_reference = None
    self.response = None

  @QtCore.Slot()
  def get_new_media_player_data(self): # Python-only slots don't need to be camel cased
    '''Synchronously run code that makes external requests to the media player in a separate thread'''

    # Using self variable because worker functions can't return
    self.response = {
      'has_track_loaded': None,
      'current_track': None,
      'player_position': None,
      'has_thread_succeded': False,
    }

    if self.scrobble_history_reference:
      self.response['has_track_loaded'] = self.scrobble_history_reference.media_player.has_track_loaded()

      if self.response['has_track_loaded']:
        self.response['current_track'] = self.scrobble_history_reference.media_player.get_current_track()
        self.response['player_position'] = self.scrobble_history_reference.media_player.get_player_position()

    # Let caller know that entire function has ran and thread hasn't been stopped midway by Qt
    self.response['has_thread_succeded'] = True

    # Emit signal to call processing function in view model
    self.finished_getting_media_player_data.emit()

class ScrobbleHistoryViewModel(QtCore.QObject):
  # Scrobble history list model signals
  pre_append_scrobble = QtCore.Signal()
  post_append_scrobble = QtCore.Signal()
  scrobble_album_image_changed = QtCore.Signal(int)

  # Thread worker signals
  get_new_media_player_data = QtCore.Signal()

  # Qt Property changed signals
  current_scrobble_data_changed = QtCore.Signal()
  current_scrobble_percentage_changed = QtCore.Signal()

  selected_scrobble_changed = QtCore.Signal()
  selected_scrobble_index_changed = QtCore.Signal()

  def __init__(self):
    QtCore.QObject.__init__(self)
    
    # Create a background thread for external requests
    self.media_player_thread = QtCore.QThread()
    self.media_player_thread.start()

    # Initialize a thread worker and move it to the background thread
    self.thread_worker = MediaPlayerThreadWorker()
    self.thread_worker.scrobble_history_reference = self
    self.thread_worker.moveToThread(self.media_player_thread)
    
    # Create passthrough signal to call get_new_media_player_data function
    self.get_new_media_player_data.connect(self.thread_worker.get_new_media_player_data)

    # Connect function to process new media player data to request finished signal
    self.thread_worker.finished_getting_media_player_data.connect(self.process_new_media_player_data)
    
    # Initialize media player plugin
    self.media_player = MockPlayerPlugin()

    # Initialize Last.fm API wrapper
    self.lastfm = LastFmApiWrapper(os.environ['LASTREDUX_LASTFM_API_KEY'], os.environ['LASTREDUX_LASTFM_CLIENT_SECRET'])
    
    # Connect to SQLite
    self.db = QtSql.QSqlDatabase.addDatabase('QSQLITE')
    self.db.setDatabaseName('db.sqlite')

    # Set Last.fm wrapper session key and username from database
    login_info = self.fetch_login_info()
    self.lastfm.set_login_info(login_info['session_key'], login_info['username'])
    
    # Store Scrobble objects that have been submitted
    self.scrobble_history = []

    # Hold a Scrobble object for currently playing track (will later be submitted)
    self.__current_scrobble = None

    # Keep track of whether the current scrobble has been submitted (both to the scrobble history and to Last.fm)
    self.__is_current_scrobble_submitted = False
    
    # Hold the index of the selected scrobble in the sidebar
    self.__selected_scrobble_index = None # -1 for current scrobble, None for no scrobble, numbers > 0 for history items
    
    # Hold the Scrobble object at the __selected_scrobble_index
    # This can either be a copy of the current scrobble or one in the history
    self.selected_scrobble = None

    # Cached data from the media player for the currently playing track
    self.__playback_data = {
      'furthest_player_position_reached': None,
      'track_start': None,
      'track_finish': None
    }

    # Start polling interval to check for new media player data
    timer = QtCore.QTimer(self)
    timer.timeout.connect(lambda: self.get_new_media_player_data.emit())
    timer.start(100)

    self.get_new_media_player_data.emit()

  # --- Qt Property Getters and Setters ---
  
  def get_current_scrobble_data(self):
    '''Return data about the currently playing track in the active media player'''
    
    if self.__current_scrobble:
      return {
        'isAdditionalDataDownloaded': self.__current_scrobble.track['is_additional_data_downloaded'],
        'name': self.__current_scrobble.track['name'],
        'artist': self.__current_scrobble.track['artist']['name'],
        'loved': False, # TODO: Request loved bool from Last.fm
        'albumImageUrl': self.__current_scrobble.track['album']['image_url_small'] # The scrobble history album arts are small so we don't want to render the full size art
      }
    
    # Return None if there isn't a curent scrobble (such as when the app is first loaded or if there is no track playing)
    return None

  def get_current_scrobble_percentage(self):
    '''Return the percentage of the track that has played compared to a user-set percentage of the track length'''

    if not self.__current_scrobble:
      return 0

    # Compensate for custom track start and end times
    # TODO: Only do this if the media player is Apple Music/iTunes
    relative_position = self.__playback_data['furthest_player_position_reached'] - self.__playback_data['track_start']
    relative_track_length = self.__playback_data['track_finish'] - self.__playback_data['track_start']
    min_scrobble_length = relative_track_length * 0.75 # TODO: Grab the percentage from the settings database
    
    # Prevent scenarios where the relative position is negative
    relative_position = max(0, relative_position)

    scrobble_percentage = relative_position / min_scrobble_length

    # Prevent scenarios where the relative player position is greater than the relative track length (don't let the percentage by greater than 1)
    scrobble_percentage = min(scrobble_percentage, 1)

    # Submit current scrobble if the scrobble percentage (progress towards the scrobble threshold) is 100%
    if not self.__is_current_scrobble_submitted and scrobble_percentage == 1:
      self.__is_current_scrobble_submitted = True
      self.submit_scrobble(self.__current_scrobble)

    return scrobble_percentage
    
  def get_selected_scrobble_index(self):
    '''Make the private selected scrobble index variable available to the UI'''
    
    if self.__selected_scrobble_index is None:
      # -2 represents no selection because Qt doesn't understand Python's None value
      return -2

    return self.__selected_scrobble_index
  
  def set_selected_scrobble_index(self, new_index):
    self.__selected_scrobble_index = new_index

    # Tell the UI that the selected index changed, so it can update the selection highlight in the sidebar to the correct index
    self.selected_scrobble_index_changed.emit()

    # Update selected_scrobble (Scrobble type) according to the new index
    if new_index == -1: # If the new selection is the current scrobble
      self.selected_scrobble = self.__current_scrobble
    else:
      self.selected_scrobble = self.scrobble_history[new_index]
    
    # Tell the UI that the selected scrobble was changed, so views like the scrobble details pane can update accordingly
    self.selected_scrobble_changed.emit()

  # --- Mock Slots ---

  @QtCore.Slot(int)
  def MOCK_playSong(self, song_num):
    self.media_player.current_track = self.media_player.SONGS[song_num]
    self.media_player.has_track_loaded_variable = True
    self.media_player.player_position = 0

  @QtCore.Slot()
  def MOCK_stopSong(self):
    self.media_player.has_track_loaded_variable = False
    self.media_player.current_track = {}

  @QtCore.Slot()
  def MOCK_moveTo75Percent(self):
    self.media_player.player_position = self.__playback_data['track_finish'] * 0.75
      
  # --- Private Functions ---

  def submit_scrobble(self, scrobble):
    '''Add a scrobble object to the history array and submit it to Last.fm'''
    
    # Tell scrobble history list model that a change will be made
    self.pre_append_scrobble.emit()

    # Prepend the new scrobble to the scrobble_history array in the view model
    self.scrobble_history.insert(0, scrobble)

    # Tell scrobble history list model that a change was made in the view model
    # The list model will call the data function in the background to get the new data
    self.post_append_scrobble.emit()

    # Shift down the selected scrobble index if new scrobble has been added to the top
    # This is because if the user has a scrobble in the history selected and a new scrobble is submitted, it will display the wrong data if the index isn't updated
    # Change __selected_scrobble_index instead of calling set___selected_scrobble_index because the selected scrobble shouldn't be redundantly set to itself and still emit selected_scrobble_changed (wasting resources)
    if self.__selected_scrobble_index and self.__selected_scrobble_index != -1:
      # Shift down the selected scrobble index by 1
      self.__selected_scrobble_index += 1

      # Tell the UI that the selected index changed, so it can update the selection highlight in the sidebar to the correct index
      self.selected_scrobble_index_changed.emit()

    # Submit scrobble to Last.fm
    ####### Thread(target=self.lastfm.submit_scrobble, args=(self.__current_scrobble,), daemon=True).start() # Trailing comma in tuple to tell Python that it's a tuple instead of an expression

  @QtCore.Slot()
  def process_new_media_player_data(self):
    response = self.thread_worker.response

    # Only run if thread actually finished and data was recieved
    if response['has_thread_succeded']:
      if response['has_track_loaded'] and response['current_track']:
        current_track = response['current_track']

        current_track_changed = (
          not self.__current_scrobble
          or not current_track['name'] == self.__current_scrobble.track['name']
          or not current_track['artist'] == self.__current_scrobble.track['artist']['name']
          or not current_track['album'] == self.__current_scrobble.track['album']['name']
        )

        if current_track_changed:
          self.__replace_current_track(current_track)
        
        # Refresh cached media player data for currently playing track
        player_position = response['player_position']

        # Only update the furthest reached position in the track if it's further than the last recorded furthest position
        # This is because if the user scrubs backward in the track, the scrobble progress bar will stop moving until they reach the previous furthest point reached in the track
        # TODO: Add support for different scrobble submission styles such as counting seconds of playback
        if player_position >= self.__playback_data['furthest_player_position_reached']:
          self.__playback_data['furthest_player_position_reached'] = player_position
        
        # Update scrobble progress bar UI
        self.current_scrobble_percentage_changed.emit()
      else: # There is no track loaded (player is stopped)
        if self.__current_scrobble:
          self.__current_scrobble = None

          # Update the UI in current scrobble sidebar item
          self.current_scrobble_data_changed.emit()

          # If the current scrobble is selected, deselect it
          if self.__selected_scrobble_index == -1:
            self.__selected_scrobble_index = None
            self.selected_scrobble = None
            
            # Update the current scrobble highlight and song details pane views
            self.selected_scrobble_index_changed.emit()
            self.selected_scrobble_changed.emit()

  def fetch_login_info(self):
    '''Fetch the user's Last.fm session key and username from the settidatabase'''

    if self.db.open():
      print('sqlite connection succeeded')
    else:
      print('sqlite connection failed')
    
    # Execute SQL to find the row that matches our criteria
    query = QtSql.QSqlQuery('SELECT value FROM settings WHERE key in ("session_key", "username")')

    # Get column id for value in settings
    idValue = query.record().indexOf("value")

    # Iterate through the list of results to get the first item, session_key
    query.next()

    # Get the value of the column of the row that we found
    session_key = query.value(idValue)

    # Iterate through the list of results to get the second item, username
    query.next()

    # Get the value of the column of the row that we found
    username = query.value(idValue)
    
    return {
      'session_key': session_key,
      'username': username
    }

  def __replace_current_track(self, current_track):
    '''Set the private __current_scrobble variable to a new Scrobble object based on the new currently playing track, update the playback data for track start and finish, and update the UI'''

    # Initialize a new Scrobble object with the currently playing track data
    # This will set the Scrobble's timestamp to the current date
    self.__current_scrobble = Scrobble(current_track['name'], current_track['artist'], current_track['album'])

    # Reset flag so new scrobble can later be submitted
    self.__is_current_scrobble_submitted = False

    # Update UI content in current scrobble sidebar item
    self.current_scrobble_data_changed.emit()

    # Reset player position to temporary value until a new value can be recieved from the media player
    self.__playback_data['furthest_player_position_reached'] = 0

    # Refresh selected_scrobble with new __current_scrobble object if the current scrobble is selected, because otherwise the selected scrobble will reflect old data
    if self.__selected_scrobble_index == -1:
      self.selected_scrobble = self.__current_scrobble

      # Update details pane view
      self.selected_scrobble_changed.emit()
    elif self.__selected_scrobble_index is None:
      self.__selected_scrobble_index = -1
      self.selected_scrobble = self.__current_scrobble
      
      # Update the current scrobble highlight and song details pane views
      self.selected_scrobble_index_changed.emit()

      # Update details pane view
      self.selected_scrobble_changed.emit()

    # Update cached media player track playback data
    self.__playback_data['track_start'] = current_track['start']
    self.__playback_data['track_finish'] = current_track['finish']

    Thread(target=self.set_additional_scrobble_data, args=(self.__current_scrobble,)).start() # Trailing comma in tuple to tell Python that it's a tuple instead of an expression

  def set_additional_scrobble_data(self, scrobble):
    '''Fetch and attach information from Last.fm to the __current_scrobble Scrobble object'''

    # Synchronously get data for scrobble from lastfm (in the separate thread this function runs in)
    track_response = self.lastfm.get_track_info(scrobble)

    # Don't try and load data for a track that doesn't exist on Last.fm yet
    # TODO: Handle rate limit condition
    if 'error' in track_response:
      return

    track_info = track_response['track'] # Response won't have a track key if it's an error

    # Get album and artist info once we know the track is in Last.fm's database
    album_info = self.lastfm.get_album_info(scrobble)['album']
    artist_info = self.lastfm.get_artist_info(scrobble)['artist']

    # Replace scrobble track property with new data
    scrobble.track = {
      'is_additional_data_downloaded': True,
      'name': scrobble.track['name'],
      'lastfm_url': track_info['url'],
      'is_loved': bool(track_info['userloved']), # Convert 1/0 to True/False
      'plays': track_info['userplaycount'],
      'tags': track_info['toptags']['tag'],

      'album': {
        'name': album_info['name'], #scrobble.track['album']['name']
        'lastfm_url': album_info['url'],
        'plays': album_info['userplaycount'],      
        'image_url': album_info['image'][4]['#text'], # Pick mega size in images array
        'image_url_small': album_info['image'][1]['#text'] # Pick medium size in images array
      },

      'artist': {
        'name': artist_info['name'],
        'lastfm_url': artist_info['url'],
        'global_listeners': artist_info['stats']['listeners'],
        'global_plays': artist_info['stats']['playcount'],
        'plays': artist_info['stats']['userplaycount'],
        'bio': artist_info['bio']['content'],
        'tags': artist_info['tags']['tag']
      }
    }

    # Update scrobble data in details pane view if it's currently showing (when the selected scrobble is the one being updated)
    if self.selected_scrobble == scrobble:
      self.selected_scrobble_changed.emit()
    
    # If scrobble is the current track, update current scrobble sidebar item to reflect actual is_loved status
    # TODO: Make separate signal that only updates is_loved data because the other data shown doesn't change
    if self.__current_scrobble == scrobble:
      self.current_scrobble_data_changed.emit()
    
    # Also update image of history item if scrobble is already in history (check every item for find index)
    for i, history_item in enumerate(self.scrobble_history):
      if history_item == scrobble:
        self.scrobble_album_image_changed.emit(i)
        # No break just in case track is somehow scrobbled twice before image loads

  # --- Qt Properties ---
  
  # Make data about the currently playing track available to the view
  currentScrobbleData = QtCore.Property('QVariant', get_current_scrobble_data, notify=current_scrobble_data_changed)

  # Make current scrobble percentage available to the view
  currentScrobblePercentage = QtCore.Property(float, get_current_scrobble_percentage, notify=current_scrobble_percentage_changed)

  # Make the current scrobble index available to the view
  selectedScrobbleIndex = QtCore.Property(int, get_selected_scrobble_index, set_selected_scrobble_index, notify=selected_scrobble_index_changed)