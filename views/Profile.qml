import QtQuick 2.14

import Kale 1.0

import 'Profile'
import '../shared/components'

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

  // --- Profile Statistics ---

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

  // --- User Link ---
  
  // Below profile statistics in code so shadow is on top
  UserLink {
    id: userLink
    
    address: isProfileLoaded && viewModel.accountDetails.lastfm_url
    imageSource: isProfileLoaded ? viewModel.accountDetails.image_url : ''
    username: isProfileLoaded ? viewModel.accountDetails.username : ''
    fullName: isProfileLoaded ? viewModel.accountDetails.real_name : ''

    anchors {
      top: parent.top
      right: parent.right
      left: parent.left
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
      isSelected: true
    }

    Tab {
      title: 'Albums'
    }
  }

  Rectangle {
    color: '#171717'

    anchors {
      top: tabs.bottom
      right: parent.right
      bottom: parent.bottom
      left: parent.left

      topMargin: 10
    }

    Flickable {
      id: flickable

      anchors.fill: parent
      
      contentWidth: parent.width
      contentHeight: column.height + 10
      clip: true

      Column {
        id: column

        anchors {
          top: parent.top
          right: parent.right
          left: parent.left
          
          topMargin: 10
          rightMargin: 15
          leftMargin: 15
        }
        
        Label {
          text: 'Top all time'
          style: kTitleTertiary
        }

        Repeater {
          model: viewModel.topArtists && viewModel.topArtists.all_time

          delegate: Row {
            Picture {
              type: kArtist

              source: modelData.image_url
            }

            Column {
              Label {
                text: modelData.name
              }
              
              Label {
                text: `Plays: ${modelData.lastfm_plays}`
              }
            }
          }
        }
      }
    }

    WheelScrollArea {
      flickable: flickable

      anchors.fill: flickable
    }

    // Shadow
    Image {
      fillMode: Image.TileHorizontally
      source: '../shared/resources/effects/tabBarShadow.png'

      height: 32

      anchors {
        top: parent.top
        right: parent.right
        left: parent.left
      }
    }

    // Border
    Rectangle {
      color: Qt.rgba(0, 0, 0, 0.17)

      height: 1

      anchors {
        top: parent.top
        right: parent.right
        left: parent.left
      }
    }
  }
}
