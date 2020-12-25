from dataclasses import dataclass
from typing import List

from datatypes.lastfm.LastfmTag import LastfmTag

@dataclass
class LastfmTags:
  tags: List[LastfmTag]

  def __str__(self) -> str:
    return f'[{", ".join([tag.__str__() for tag in self.tags])}]'