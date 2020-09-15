import QtQuick 2.14

import Kale 1.0

import 'Profile'

Item {
  id: root

  property ProfileViewModel viewModel

  property bool areUserStatisticsLoaded: {
    if (viewModel) {
      return !!viewModel.userStatistics
    }

    return false
  }

  // When the StackView switches to this tab, request date for the profile view
  Component.onCompleted: {
    if (viewModel) {
      viewModel.loadUserStatistics()
    }
  }

  // --- User Link ---
  
  UserLink {
    id: userLink
    
    address: areUserStatisticsLoaded && viewModel.userInfo.lastfm_url
    imageSource: areUserStatisticsLoaded ? viewModel.userInfo.image_url : ''
    fullName: areUserStatisticsLoaded ? viewModel.userInfo.real_name : 'Loading...'
    username: areUserStatisticsLoaded ? viewModel.userInfo.username : 'Loading...'

    anchors {
      top: parent.top
      right: parent.right
      left: parent.left

      topMargin: 10
    }
  }

  Column {
    id: profileStatistics
    
    spacing: 8

    anchors {
      top: userLink.bottom
      right: parent.right
      left: parent.left

      topMargin: 10
      rightMargin: 15
      leftMargin: 15
    }

    // --- Scrobbles ---

    ProfileStatistic {
      iconName: 'scrobble'
      value: areUserStatisticsLoaded && viewModel.userStatistics.total_scrobbles
      caption: 'scrobbles'

      width: parent.width
    }

    // --- Scrobbles Today ---

    ProfileStatistic {
      iconName: 'clock'
      value: areUserStatisticsLoaded && viewModel.userStatistics.total_scrobbles_today
      caption: 'plays today'

      width: parent.width
    }
    
    // --- Scrobbles Per Day ---

    ProfileStatistic {
      iconName: 'calendar'
      value: areUserStatisticsLoaded && viewModel.userStatistics.average_daily_scrobbles
      caption: 'plays per day'

      width: parent.width
    }

    // --- Artists in Library ---

    ProfileStatistic {
      iconName: 'artist'
      value: areUserStatisticsLoaded && viewModel.userStatistics.total_artists
      caption: 'artists in library'

      width: parent.width
    }

    // --- Loved Tracks ---

    ProfileStatistic {
      iconName: 'heart'
      value: areUserStatisticsLoaded && viewModel.userStatistics.total_loved_tracks
      caption: 'loved tracks'

      width: parent.width
    }
  }

  // --- Tabs ---

  Row {
    id: tabs

    spacing: 5

    anchors {
      horizontalCenter: parent.horizontalCenter

      top: profileStatistics.bottom

      topMargin: 15
    }

    Tab {
      title: 'Tracks'
    }

    Tab {
      title: 'Artists'
    }

    Tab {
      title: 'Albums'
    }
  }
}
