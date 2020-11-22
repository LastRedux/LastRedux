from typing import List

from datatypes.ListeningStatistic import ListeningStatistic

def listening_statistics_with_percentages(listening_statistics: List[ListeningStatistic]):
  '''Calculate the relative percentages of each statistic relative to the highest playcount in a list of statistics ordered by playcount descending'''
  
  # The first item has the most plays
  highest_playcount = listening_statistics[0].plays

  for listening_statistic in listening_statistics:
    listening_statistic.plays_percentage = listening_statistic.plays / highest_playcount

  return listening_statistics