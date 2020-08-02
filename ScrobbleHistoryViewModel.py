import time

from PySide2 import QtCore
from plugins.AppleMusicPlugin import AppleMusicPlugin

from models import Scrobble

class ScrobbleHistoryViewModel(QtCore.QObject):
  # Scrobble history list model signals
  pre_append_scrobble = QtCore.Signal()
  post_append_scrobble = QtCore.Signal()

  # Qt Property changed signals
  current_scrobble_data_changed = QtCore.Signal()
  current_scrobble_percentage_changed = QtCore.Signal()

  selected_scrobble_changed = QtCore.Signal()
  selected_scrobble_index_changed = QtCore.Signal()

  def __init__(self):
    QtCore.QObject.__init__(self)

    self.media_player = AppleMusicPlugin()
    
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

    self.getNewMediaPlayerData()

  # --- Qt Property Getters and Setters ---
  
  def get_current_scrobble_data(self):
    '''Return data about the currently playing track in the active media player'''
    
    if self.__current_scrobble:
      return {
        'name': self.__current_scrobble.track['name'],
        'artist': self.__current_scrobble.track['artist']['name'],
        'loved': False # TODO: Request loved bool from Last.fm
      }
    
    # TODO: Detect when nothing playing

    # Return an empty scrobble data object if there isn't a curent scrobble (such as when the app is first loaded or if there is no track playing)
    return {
      'name': '',
      'artist': ''
    }

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
      self.submitScrobble(self.__current_scrobble)

    return scrobble_percentage
    
  def get_selected_scrobble_index(self):
    '''Make the private selected scrobble index variable available to the UI'''
    
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

  # --- Slots ---

  @QtCore.Slot()
  def submitScrobble(self, scrobble):
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
      time.sleep(5)
      self.__selected_scrobble_index += 1

      # Tell the UI that the selected index changed, so it can update the selection highlight in the sidebar to the correct index
      self.selected_scrobble_index_changed.emit()

  @QtCore.Slot()
  def getNewMediaPlayerData(self):
    if self.media_player.has_track_loaded():
      current_track = self.media_player.get_current_track()

      current_track_changed =  (
        not self.__current_scrobble
        or not current_track['name'] == self.__current_scrobble.track['name']
        or not current_track['artist'] == self.__current_scrobble.track['artist']['name']
        or not current_track['album'] == self.__current_scrobble.track['album']['name']
      )

      if current_track_changed:
        self.__replace_current_track(current_track)
      
      # Refresh cached media player data for currently playing track
      player_position = self.media_player.get_player_position()

      # Only update the furthest reached position in the track if it's further than the last recorded furthest position
      # This is because if the user scrubs backward in the track, the scrobble progress bar will stop moving until they reach the previous furthest point reached in the track
      # TODO: Add support for different scrobble submission styles such as counting seconds of playback
      if player_position > self.__playback_data['furthest_player_position_reached']:
        self.__playback_data['furthest_player_position_reached'] = player_position
      
      # Update scrobble progress bar UI
      self.current_scrobble_percentage_changed.emit()
      
  # --- Private Functions ---
      
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

      # Update UI content in details pane
      self.selected_scrobble_changed.emit()

    # Update cached media player track playback data
    self.__playback_data['track_start'] = current_track['start']
    self.__playback_data['track_finish'] = current_track['finish']

  # --- Qt Properties ---
  
  # Make data about the currently playing track available to the view
  currentScrobbleData = QtCore.Property('QVariant', get_current_scrobble_data, notify=current_scrobble_data_changed)

  # Make current scrobble percentage available to the view
  currentScrobblePercentage = QtCore.Property(float, get_current_scrobble_percentage, notify=current_scrobble_percentage_changed)

  # Make the current scrobble index available to the view
  selectedScrobbleIndex = QtCore.Property(int, get_selected_scrobble_index, set_selected_scrobble_index, notify=selected_scrobble_index_changed)