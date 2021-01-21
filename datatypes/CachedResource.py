from datetime import datetime
from dataclasses import dataclass
from typing import TypeVar, Generic

T = TypeVar('T')

@dataclass
class CachedResource(Generic[T]):
  data: T
  expiration_date: datetime