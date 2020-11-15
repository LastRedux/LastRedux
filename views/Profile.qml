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
      address: isProfileLoaded && `https://www.last.fm/user/${viewModel.accountDetails.username}/library`
      iconName: 'scrobble'
      value: isProfileLoaded && viewModel.profileStatistics.total_scrobbles
      caption: 'scrobbles'

      width: parent.width
    }

    // --- Scrobbles Today ---

    ProfileStatistic {
      property string currentDate: {
        const today = new Date()
        return `${today.getFullYear()}-${today.getMonth() + 1}-${today.getDate()}`
      }

      address: isProfileLoaded && `https://www.last.fm/user/${viewModel.accountDetails.username}/library?from=${currentDate}&to=${currentDate}`
      iconName: 'clock'
      value: isProfileLoaded && viewModel.profileStatistics.total_scrobbles_today
      caption: 'plays today'

      width: parent.width
    }
    
    // --- Scrobbles Per Day ---

    ProfileStatistic {
      address: isProfileLoaded && `https://www.last.fm/user/${viewModel.accountDetails.username}/library`
      iconName: 'calendar'
      value: isProfileLoaded && viewModel.profileStatistics.average_daily_scrobbles
      caption: 'plays per day'

      width: parent.width
    }

    // --- Artists in Library ---

    ProfileStatistic {
      address: isProfileLoaded && `https://www.last.fm/user/${viewModel.accountDetails.username}/library/artists`
      iconName: 'artist'
      value: isProfileLoaded && viewModel.profileStatistics.total_artists
      caption: 'artists in library'

      width: parent.width
    }

    // --- Loved Tracks ---

    ProfileStatistic {
      address: isProfileLoaded && `https://www.last.fm/user/${viewModel.accountDetails.username}/loved`
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
    backgroundImageSource: isProfileLoaded ? viewModel.accountDetails.large_image_url : ''
    username: isProfileLoaded ? viewModel.accountDetails.username : ''
    fullName: isProfileLoaded ? viewModel.accountDetails.real_name : ''

    anchors {
      top: parent.top
      right: parent.right
      left: parent.left
    }
  }

  // --- Tabs ---

  // Row {
  //   id: tabs

  //   spacing: 5

  //   anchors {
  //     horizontalCenter: parent.horizontalCenter

  //     top: profileStatistics.bottom

  //     topMargin: 15
  //   }

  //   Tab {
  //     title: 'Tracks'
  //   }

  //   Tab {
  //     title: 'Artists'
  //     isSelected: true
  //   }

  //   Tab {
  //     title: 'Albums'
  //   }
  // }

  Rectangle {
    color: '#171717'

    anchors {
      top: profileStatistics.bottom
      right: parent.right
      bottom: parent.bottom
      left: parent.left

      topMargin: 10
    }

    Flickable {
      id: flickable

      anchors.fill: parent
      
      contentWidth: parent.width
      contentHeight: column.y + column.height + 10
      clip: true

      Column {
        id: column

        spacing: 15

        anchors {
          top: parent.top
          right: parent.right
          left: parent.left
          
          topMargin: 10
        }
        
        Column {
          spacing: 8

          width: parent.width

          Label {
            text: 'Top Artists This Week'
            style: kTitleTertiary

            x: 15
          }

          Column {
            spacing: 10

            width: parent.width

            Repeater {
              model: viewModel.topArtists && viewModel.topArtists.last_7_days

              delegate: ListeningStatistic {
                hasImage: modelData.has_image
                imageSource: modelData.image_url
                lastfmUrl: modelData.lastfm_url
                title: modelData.title
                scrobbleCount: modelData.lastfm_plays
                scrobbleCountPercentage: modelData.percentage

                width: flickable.width
              }
            }
          }
        }

        Column {
          spacing: 8

          width: parent.width

          Label {
            text: 'Top Artists Overall'
            style: kTitleTertiary

            x: 15
          }

          Column {
            spacing: 10

            width: parent.width

            Repeater {
              model: viewModel.topArtists && viewModel.topArtists.all_time

              delegate: ListeningStatistic {
                hasImage: modelData.has_image
                imageSource: modelData.image_url
                lastfmUrl: modelData.lastfm_url
                title: modelData.title
                scrobbleCount: modelData.lastfm_plays
                scrobbleCountPercentage: modelData.percentage

                width: flickable.width
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
      color: Qt.rgba(0, 0, 0, 0.23)

      height: 1

      anchors {
        top: parent.top
        right: parent.right
        left: parent.left
      }
    }
  }
}
