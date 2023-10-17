from PySide6 import QtCore

from datatypes.TrackCrop import TrackCrop

class FetchTrackCrop(QtCore.QObject, QtCore.QRunnable):
  finished = QtCore.Signal(TrackCrop)

  def __init__(self, applescript_music_app) -> None:
    QtCore.QObject.__init__(self)
    QtCore.QRunnable.__init__(self)
    self.__applescript_music_app = applescript_music_app
    self.setAutoDelete(True)

  def run(self) -> None:
    '''
    Use AppleScript to fetch the current track's start and finish timestamps
    Note: This often fails and returns 0.0 for both
    '''

    current_track = self.__applescript_music_app.currentTrack()
    
    track_crop = TrackCrop(
      start=current_track.start(),
      finish=current_track.finish()
    )

    self.finished.emit(track_crop)