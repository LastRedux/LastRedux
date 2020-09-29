import QtQuick 2.14

import Kale 1.0

import 'Profile'

Item {
  id: root

  property ProfileViewModel viewModel

  property bool isProfileLoaded: {
    if (viewModel) {
      return !!(viewModel.accountDetails && viewModel.profileStatistics)
    }

    return false
  }

  // When the StackView switches to this tab, request data for the profile default view
  Component.onCompleted: {
    if (viewModel) {
      viewModel.loadProfileAndTopArtists()
    }
  }

  // --- User Link ---
  
  UserLink {
    id: userLink
    
    address: isProfileLoaded && viewModel.accountDetails.lastfm_url
    imageSource: isProfileLoaded ? viewModel.accountDetails.image_url : ''
    fullName: isProfileLoaded ? viewModel.accountDetails.real_name : 'Loading...'
    username: isProfileLoaded ? viewModel.accountDetails.username : 'Loading...'

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
      value: isProfileLoaded && viewModel.profileStatistics.total_scrobbles
      caption: 'scrobbles'

      width: parent.width
    }

    // --- Scrobbles Today ---

    ProfileStatistic {
      iconName: 'clock'
      value: isProfileLoaded && viewModel.profileStatistics.total_scrobbles_today
      caption: 'plays today'

      width: parent.width
    }
    
    // --- Scrobbles Per Day ---

    ProfileStatistic {
      iconName: 'calendar'
      value: isProfileLoaded && viewModel.profileStatistics.average_daily_scrobbles
      caption: 'plays per day'

      width: parent.width
    }

    // --- Artists in Library ---

    ProfileStatistic {
      iconName: 'artist'
      value: isProfileLoaded && viewModel.profileStatistics.total_artists
      caption: 'artists in library'

      width: parent.width
    }

    // --- Loved Tracks ---

    ProfileStatistic {
      iconName: 'heart'
      value: isProfileLoaded && viewModel.profileStatistics.total_loved_tracks
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
