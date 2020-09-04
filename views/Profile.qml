import QtQuick 2.14

import Kale 1.0

import 'Profile'

Item {
  id: root

  property ProfileViewModel viewModel

  property bool isUserInfoLoaded: {
    if (viewModel) {
      return !!viewModel.userInfo
    }

    return false
  }

  Component.onCompleted: {
    if (viewModel) {
      viewModel.loadUserInfoAndArtistListeningStatistics()
    }
  }

  // --- User Link ---
  
  UserLink {
    id: userLink
    
    address: isUserInfoLoaded && viewModel.userInfo.lastfm_url
    imageSource: isUserInfoLoaded ? viewModel.userInfo.image_url : ''
    fullName: isUserInfoLoaded ? viewModel.userInfo.real_name : 'Loading...'
    username: isUserInfoLoaded ? viewModel.userInfo.username : 'Loading...'

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
      value: isUserInfoLoaded && viewModel.userInfo.total_scrobbles
      caption: 'scrobbles'

      width: parent.width
    }

    // --- Scrobbles Per Day ---

    ProfileStatistic {
      iconName: 'clock'
      value: isUserInfoLoaded && viewModel.userInfo.average_daily_scrobbles
      caption: 'scrobbles per day'

      width: parent.width
    }

    // --- Artists in Library ---

    ProfileStatistic {
      iconName: 'artist'
      value: isUserInfoLoaded && viewModel.userInfo.total_artists
      caption: 'artists in library'

      width: parent.width
    }

    // --- Loved Tracks ---

    ProfileStatistic {
      iconName: 'heart'
      value: isUserInfoLoaded && viewModel.userInfo.total_artists
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