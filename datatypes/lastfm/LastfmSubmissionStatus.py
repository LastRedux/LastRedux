from dataclasses import dataclass

@dataclass
class LastfmSubmissionStatus:
  accepted_count: int = 0
  ignored_count: int = 0

  '''
  Ignored error codes:
  1: Artist was ignored
  2: Track was ignored
  3: Timestamp was too old
  4: Timestamp was too new
  5: Daily scrobble limit exceeded
  '''
  ignored_error_code: int = None