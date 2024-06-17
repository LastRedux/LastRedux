from dataclasses import dataclass
from typing import List

from .LastfmArtistLink import LastfmArtistLink
from .LastfmTag import LastfmTag
from datatypes.ImageSet import ImageSet


@dataclass
class LastfmAlbum:
    url: str
    title: str
    artist_link: LastfmArtistLink
    image_set: ImageSet
    plays: int

    # TODO: Actually display this data
    global_listeners: int = None
    global_plays: int = None
    tags: List[LastfmTag] = None

    def __str__(self) -> str:
        return "\n".join(
            (
                f"{repr(self)} [{self.plays}]",
                f"Global Listeners: {self.global_listeners}",
                f"Global Plays: {self.global_plays}",
                f"Tags: {self.tags}",
            )
        )

    def __repr__(self) -> str:
        return f"{self.title} | {self.artist_link.name}"
