from dataclasses import asdict
from typing import List
from datetime import datetime

from PySide6 import QtCore

from util.lastfm import LastfmApiWrapper, LastfmArtist
from datatypes.ProfileStatistic import ProfileStatistic
from datatypes.ProfileStatistics import ProfileStatistics


def artists_to_profile_statistics(artists: List[LastfmArtist]):
    top_plays = artists[0].plays

    return [
        ProfileStatistic(
            title=artist.name,
            plays=artist.plays,
            percentage=artist.plays / top_plays,
            lastfm_url=artist.url,
            image_url=None,  # Artist images are loaded separately
        )
        for artist in artists
    ]


class FetchProfileStatistics(QtCore.QObject, QtCore.QRunnable):
    finished = QtCore.Signal(ProfileStatistics)

    def __init__(self, lastfm: LastfmApiWrapper) -> None:
        QtCore.QObject.__init__(self)
        QtCore.QRunnable.__init__(self)
        self.lastfm = lastfm
        self.setAutoDelete(True)

    def run(self) -> None:
        """Fetch user info, top artists and generate user statistics"""

        profile_statistics = None
        user_info = self.lastfm.get_user_info()

        # Skip other requests if user_info came back blank (we're offline)
        if user_info:
            top_artists = self.lastfm.get_top_artists(limit=5)
            top_artists_week = self.lastfm.get_top_artists(limit=5, period="7day")

            profile_statistics = ProfileStatistics(
                total_scrobbles_today=self.lastfm.get_total_scrobbles_today(),
                total_artists=top_artists.attr_total,
                total_loved_tracks=self.lastfm.get_total_loved_tracks(),
                average_daily_scrobbles=round(
                    user_info.total_scrobbles
                    / (datetime.now() - user_info.registered_date).days
                ),
                top_artists=(
                    artists_to_profile_statistics(top_artists.items)
                    if top_artists.attr_total
                    else None
                ),
                top_artists_week=(
                    artists_to_profile_statistics(top_artists_week.items)
                    if top_artists_week.attr_total
                    else None
                ),
                **asdict(user_info)
            )

        self.finished.emit(profile_statistics)
