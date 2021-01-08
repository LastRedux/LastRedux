from datetime import datetime
from dataclasses import dataclass

from datatypes.lastfm.LastfmUser import LastfmUser

@dataclass
class LastfmUserInfo(LastfmUser):
  total_scrobbles: int
  registered_date: datetime
  
  def __str__(self) -> str:
    return '\n'.join((
      f'Username: {self.username}',
      f'Name: {self.real_name or "N/A"}',
      f'Profile: {self.url}',
      f'Image: {self.image_url}',
      f'Registered: {self.registered_date.strftime("%Y-%m-%d %H:%M:%S")}',
      f'Scrobbles: {self.total_scrobbles}'
    ))