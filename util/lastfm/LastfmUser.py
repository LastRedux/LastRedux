from _future_ import annotations
from dataclasses import dataclass

@dataclass
class LastfmUser:
  url: str
  username: str
  real_name: str
  image_url: str # There's only one size for friend images

  def __str__(self) -> str:
    return '\n'.join((
      f'Username: {self.username}',
      f'Name: {self.real_name or "N/A"}',
      f'Profile: {self.url}'
    ))

  def __repr__(self) -> str:
    return self.username