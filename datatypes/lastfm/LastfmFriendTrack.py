from dataclasses import dataclass

from datatypes.lastfm.LastfmHistoryTrack import LastfmHistoryTrack

@dataclass
class LastfmFriendTrack(LastfmHistoryTrack):
  is_now_playing: bool