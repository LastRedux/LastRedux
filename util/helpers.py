import datetime
import subprocess
import json

from AppKit import NSScreen
import psutil

from util.lastfm.LastfmList import LastfmList
from util.lastfm.LastfmScrobble import LastfmScrobble


def get_mock_recent_scrobbles(count: int) -> LastfmList[LastfmScrobble]:
    return LastfmList(
        items=[
            LastfmScrobble(
                artist_name=mock_track["artist_name"],
                track_title=mock_track["track_title"],
                album_title=mock_track.get("album_title", None),
                album_artist_name=mock_track.get(
                    "artist_name", None
                ),  # TODO: Use an actual album artist for mock tracks
                timestamp=datetime.datetime.now() - datetime.timedelta(minutes=3 * i),
            )
            for i, mock_track in enumerate(
                json.load(open("mock_data/mock_tracks.json"))[1 : count + 1]
            )
            if mock_track.get("artist_name")
        ],
        attr_total=count,
    )


def generate_system_profile() -> dict:
    software_info = json.loads(
        subprocess.check_output("system_profiler SPSoftwareDataType -json", shell=True)
    )["SPSoftwareDataType"][0]
    software_string = " ".join(
        (
            software_info["os_version"],
            software_info["system_integrity"],
            software_info["uptime"],
        )
    )

    hardware_info = json.loads(
        subprocess.check_output("system_profiler SPHardwareDataType -json", shell=True)
    )["SPHardwareDataType"][0]
    hardware_string = " ".join(
        (
            hardware_info["machine_model"],
            hardware_info.get(
                "cpu_type", hardware_info.get("chip_type", "Unknown CPU type")
            ),
            hardware_info["physical_memory"],
            hardware_info.get(
                "current_processor_speed", "Unknown current processor speed"
            ),
        )
    )

    return {
        "software": software_string,
        "hardware": hardware_string,
        "displays": f"""{[f'{int(screen.frame().size.width)}x{int(screen.frame().size.height)} {"(Retina)" if screen.backingScaleFactor() == 2.0 else ""}' for screen in NSScreen.screens()]}""",
    }


def is_within_24_hours(date: datetime.datetime) -> bool:
    return (
        datetime.datetime.now() - date
    ).total_seconds() <= 86400  # 24 hours = 86400 seconds


def is_discord_open() -> bool:
    """Check if there is a process named Discord running"""

    # TODO: Find a way to make this less fallible (ie. fake Discord app will crash LastRedux)
    return "Discord" in [process.name() for process in psutil.process_iter()]
