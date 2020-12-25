from dataclasses import dataclass

@dataclass
class MediaPlayerState:
  is_playing: bool
  track_title: str
  artist_name: str
  album_title: str
  track_start: float = 0.0
  track_finish: float = None

  @staticmethod
  def build_from_applescript_track(track, is_playing):
    return MediaPlayerState(
      is_playing=is_playing,
      track_title=track.name(),
      artist_name=track.artist(),
      album_title=track.album(), # TODO: Make sure this isn't going to cause problems without a fallback
      track_start=0,
      track_finish=track.duration() / 1000 # Convert from ms to s
    )