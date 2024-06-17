from dataclasses import dataclass


@dataclass
class ImageSet:
    small_url: str
    medium_url: str

    def __bool__(self) -> bool:
        return self.small_url is not None and self.medium_url is not None
