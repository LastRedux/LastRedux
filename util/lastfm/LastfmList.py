from dataclasses import dataclass
from typing import List, TypeVar, Generic

T = TypeVar("T")


@dataclass
class LastfmList(Generic[T]):
    items: List[T]

    """
    How many items exist matching the criteria of the request that returned this list of items

    Example: Request to user.getRecentTracks with a limit of 5 and period of overall returns 5 items but will have an @attr total of the number of tracks the user has ever scrobbled (19,000 for example)
    """
    attr_total: int

    def __str__(self) -> str:
        return "[" + ", ".join([repr(item) for item in self.items]) + "]"
