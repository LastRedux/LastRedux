from dataclasses import dataclass

from datatypes import ImageSet

@dataclass
class LastfmUser:
  url: str
  username: str
  real_name: str
  image_url: str

  def __str__(self) -> str:
    return '\n'.join((
      f'Username: {self.username}',
      f'Name: {self.real_name or "N/A"}',
      f'Profile: {self.url}'
    ))