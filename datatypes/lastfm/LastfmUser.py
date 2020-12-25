from dataclasses import dataclass

@dataclass
class LastfmUser:
  username: str
  real_name: str
  image_url: str
  image_url_small: str
  url: str

  def __str__(self) -> str:
    return '\n'.join((
      f'Username: {self.username}',
      f'Name: {self.real_name or "N/A"}',
      f'Image: {self.image_url}',
      f'Profile: {self.url}'
    ))