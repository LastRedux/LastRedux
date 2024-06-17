from dataclasses import dataclass


@dataclass
class SimpleTrack:
    artist_name: str
    track_title: str
    album_title: str
    album_artist_name: str

    def __str__(self) -> str:
        string = f"{self.artist_name} - {self.track_title}"

        if self.album_title:
            string += f" | {self.album_title}"

        return string

    def __repr__(self):
        return str(self)
