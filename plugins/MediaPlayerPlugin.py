# Base class for interfacing with media players
class MediaPlayerPlugin():
  def __init__(self):
    pass

  def has_track_loaded(self):
    pass

  def get_current_track(self):
    pass

  def get_player_position(self):
    pass