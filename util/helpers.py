from datetime import datetime
import subprocess
import json
from typing import List

from AppKit import NSScreen

from datatypes.ListeningStatistic import ListeningStatistic

def listening_statistics_with_percentages(listening_statistics: List[ListeningStatistic]):
  '''Calculate the relative percentages of each statistic relative to the highest playcount in a list of statistics ordered by playcount descending'''
  
  # The first item has the most plays
  highest_playcount = listening_statistics[0].plays

  for listening_statistic in listening_statistics:
    listening_statistic.plays_percentage = listening_statistic.plays / highest_playcount

  return listening_statistics

def generate_system_profile():
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

def is_within_24_hours(date: datetime):
  return (datetime.now() - date).total_seconds() <= 86400 # 24 hours = 86400 seconds