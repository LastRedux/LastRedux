from dataclasses import dataclass

@dataclass
class LastfmUpdateNowPlayingStatus:
  # See LastfmScrobbleStatus for error code meanings
  ignored_error_code: int