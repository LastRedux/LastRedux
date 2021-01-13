from datetime import datetime
import subprocess
import json
from typing import List

from AppKit import NSScreen

from util.lastfm.LastfmScrobble import LastfmScrobble

def get_mock_recent_scrobbles(count: int) -> List[LastfmScrobble]:
  return [
    LastfmScrobble(
      artist_name=mock_track['artist_name'],
      track_title=mock_track['track_title'],
      album_title=mock_track.get('album_title', None),
      timestamp=datetime.datetime.now() - datetime.timedelta(minutes=3 * i)
    ) for i, mock_track in enumerate(
      json.load(open('mock_data/mock_tracks.json'))[1:count]
    ) if mock_track.get('artist_name')
  ]

def generate_system_profile() -> dict:
  software_info = json.loads(subprocess.check_output('system_profiler SPSoftwareDataType -json', shell=True))['SPSoftwareDataType'][0]
  software_string = ' '.join((
    software_info['os_version'],
    software_info['system_integrity'],
    software_info['uptime']
  ))

  hardware_info = json.loads(subprocess.check_output('system_profiler SPHardwareDataType -json', shell=True))['SPHardwareDataType'][0]
  hardware_string = ' '.join((
    hardware_info['machine_model'],
    hardware_info['cpu_type'],
    hardware_info['physical_memory'],
    hardware_info['current_processor_speed'],
  ))

  return {
    'software': software_string,
    'hardware': hardware_string,
    'displays': f'''{[f'{int(screen.frame().size.width)}x{int(screen.frame().size.height)} {"(Retina)" if screen.backingScaleFactor() == 2.0 else ""}' for screen in NSScreen.screens()]}'''
  }

def is_within_24_hours(date: datetime) -> bool:
  return (datetime.now() - date).total_seconds() <= 86400 # 24 hours = 86400 seconds