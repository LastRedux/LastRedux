from datetime import datetime
import threading

from PySide2 import QtCore, QtGui

# TODO: Move Objective-C imports and related code to separate Apple Music plugin class
from Foundation import *
from ScriptingBridge import *

class Scrobble:
  def __init__(self, track, artist='Artist Name', album='Album Name'):
    # Provided by Apple Music
    self.track = track
    self.artist = artist
    self.album = album
    self.timestamp = datetime.now()

    # Provided by Last.fm
    self.isLoved = False
    self.tags = []
    self.playCount = None
    self.url = None
    self.albumUrl = None

    self.artistUrl = None
    self.artistListeners = None
    self.artistPlays = None
    self.artistPlaysInLibrary = None
    self.artistBio = None
    self.artistTags = []

class ApplicationViewModel(QtCore.QObject):
  # List model signals
  pre_add_scrobble = QtCore.Signal()
  post_add_scrobble = QtCore.Signal()

  # Property signals
  current_scrobble_changed = QtCore.Signal()
  current_scrobble_percentage_changed = QtCore.Signal()
  selected_scrobble_changed = QtCore.Signal()
  selected_scrobble_index_changed = QtCore.Signal()

  def __init__(self):
    QtCore.QObject.__init__(self)
    
    self.current_scrobble = None
    self.selected_scrobble = None

    # Get reference to Apple Music application
    self.apple_music = SBApplication.applicationWithBundleIdentifier_("com.apple.Music")
    self.selected_scrobble_index = None
    self.is_current_track_scrobbled = False
    self.player_position = None
    self.track_start = None
    self.track_finish = None
    self.checkForNewTrack()
    self.scrobble_history = []

  @QtCore.Slot()
  def checkForNewTrack(self):
    APPLE_MUSIC_IS_STOPPED_CODE = 1800426323 # From Music.app BridgeSupport enum definitions

    if self.apple_music.playerState() == APPLE_MUSIC_IS_STOPPED_CODE:
      if self.current_scrobble:
        if self.selected_scrobble_index == -1:
          self.selected_scrobble_index = None
          self.selected_scrobble_index_changed.emit()
          self.selected_scrobble_changed.emit()

        self.current_scrobble = None
        self.current_scrobble_changed.emit()
    else:
      current_track_reference = self.apple_music.currentTrack()

      current_track = {
        'track': current_track_reference.name(),
        'artist': current_track_reference.artist(),
        'album': current_track_reference.album(),
        'player_position': self.apple_music.playerPosition(),

        # Compensate for cropped tracks
        'start': current_track_reference.start(),
        'finish': current_track_reference.finish()
      }

      if (
        not self.current_scrobble
        or not current_track['track'] ==  self.current_scrobble.track
        or not current_track['artist'] == self.current_scrobble.artist
        or not current_track['album'] == self.current_scrobble.album
      ):
        # New track is playing
        self.current_scrobble = Scrobble(current_track['track'], current_track['artist'], current_track['album'])
        self.current_scrobble_changed.emit()
        self.is_current_track_scrobbled = False
        self.player_position = 0

        if self.selected_scrobble_index == -1:
          self.selected_scrobble = self.current_scrobble
          self.selected_scrobble_changed.emit()
      
      if not self.player_position or current_track['player_position'] > self.player_position:
        self.player_position = current_track['player_position']
      
      self.track_start = current_track['start']
      self.track_finish = current_track['finish']
      self.current_scrobble_percentage_changed.emit()
  
  @QtCore.Slot()
  def addScrobble(self, scrobble):
    self.pre_add_scrobble.emit()
    self.scrobble_history.insert(0, scrobble)
    self.post_add_scrobble.emit()

    if self.selected_scrobble_index != -1:
      self.selected_scrobble_index += 1
      self.selected_scrobble_index_changed.emit()
  
  @QtCore.Slot(int)
  def selectScrobble(self, index):
    self.selected_scrobble_changed.emit()
  
  # Current scrobble metadata
  # def get_current_scrobble_track(self):
  #   return self.current_scrobble.track
  
  # def get_current_scrobble_artist(self):
  #   return self.current_scrobble.artist
  def get_current_scrobble(self):
    if self.current_scrobble:
      return {
        'track': self.current_scrobble.track,
        'artist': self.current_scrobble.artist
      }
    
    return {
      'track': '',
      'artist': ''
    }
  
  def get_current_scrobble_percentage(self):
    if self.current_scrobble:
      percentage = max(0, min((self.player_position - self.track_start) / ((self.track_finish * 0.75) - self.track_start), 1))

      if not self.is_current_track_scrobbled and percentage == 1:
        self.addScrobble(self.current_scrobble)
        self.is_current_track_scrobbled = True

      return percentage
    
    return 0
  
  # Selected scrobble index
  def get_selected_scrobble_index(self):
    return self.selected_scrobble_index
  
  def set_selected_scrobble_index(self, index):
    self.selected_scrobble_index = index
    self.selected_scrobble_index_changed.emit()

    if index > -1:
      self.selected_scrobble = self.scrobble_history[index]
    else:
      self.selected_scrobble = self.current_scrobble

    self.selected_scrobble_changed.emit()
  
  # Proprerties
  # currentScrobbleTrack = QtCore.Property(str, get_current_scrobble_track, notify=current_scrobble_changed)
  # currentScrobbleArtist = QtCore.Property(str, get_current_scrobble_artist, notify=current_scrobble_changed)
  currentScrobble = QtCore.Property('QVariant', get_current_scrobble, notify=current_scrobble_changed)
  currentScrobblePercentage = QtCore.Property(float, get_current_scrobble_percentage, notify=current_scrobble_percentage_changed)
  selectedScrobbleIndex = QtCore.Property(int, get_selected_scrobble_index, set_selected_scrobble_index, notify=selected_scrobble_index_changed)
