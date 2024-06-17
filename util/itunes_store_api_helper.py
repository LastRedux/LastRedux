import urllib

import requests

from datatypes.ImageSet import ImageSet


def get_album_art(
    artist_name: str, track_title: str, album_title: str = None
) -> ImageSet:
    """Get album art for Apple Music tracks through the iTunes Search API"""

    # Escape special characters in query string
    escaped_search_term = urllib.parse.quote(
        f"{artist_name} {track_title} {album_title}"
    )

    # Do a generic search for music with the track, artist, and album name
    track_response = requests.get(
        f"https://itunes.apple.com/search?media=music&limit=1&term={escaped_search_term}"
    )

    if not track_response.ok:
        raise Exception(f"Error getting iTunes store images: {track_response.text}")

    track_results = track_response.json()["results"]

    # Return an empty object if there are no results for the track (local file)
    if not track_results:
        return

    return ImageSet(
        small_url=track_results[0]["artworkUrl30"].replace("30x30", "64x64"),
        medium_url=track_results[0]["artworkUrl30"].replace("30x30", "300x300"),
    )
