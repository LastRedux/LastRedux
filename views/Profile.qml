import QtQuick 2.14

import Kale 1.0

import 'Profile'
import '../shared/components'

Item {
  id: root

  property ProfileViewModel viewModel

  property bool isProfileLoaded: {
    if (viewModel) {
      return !!(viewModel.profileStatistics)
    }

    return false
  }

  // --- Profile Statistics ---

  Column {
    id: userStatistics
    
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

    UserStatistic {
      address: isProfileLoaded && viewModel.profileStatistics.url
      iconName: 'scrobble'
      value: isProfileLoaded ? viewModel.profileStatistics.total_scrobbles : undefined
      caption: 'scrobbles'

      width: parent.width
    }

    // --- Scrobbles Today ---

    UserStatistic {
      property string currentDate: {
        const today = new Date()
        return `${today.getFullYear()}-${today.getMonth() + 1}-${today.getDate()}`
      }

      address: isProfileLoaded && `https://www.last.fm/user/${viewModel.profileStatistics.username}/library?from=${currentDate}&to=${currentDate}`
      iconName: 'clock'
      value: isProfileLoaded ? viewModel.profileStatistics.total_scrobbles_today : undefined
      caption: 'plays today'

      width: parent.width
    }
    
    // --- Scrobbles Per Day ---

    UserStatistic {
      address: isProfileLoaded && `https://www.last.fm/user/${viewModel.profileStatistics.username}/library`
      iconName: 'calendar'
      value: isProfileLoaded ? viewModel.profileStatistics.average_daily_scrobbles : undefined
      caption: 'plays per day'

      width: parent.width
    }

    // --- Artists in Library ---

    UserStatistic {
      address: isProfileLoaded && `https://www.last.fm/user/${viewModel.profileStatistics.username}/library/artists`
      iconName: 'artist'
      value: isProfileLoaded ? viewModel.profileStatistics.total_artists : undefined
      caption: 'artists in library'

      width: parent.width
    }

    // --- Loved Tracks ---

    UserStatistic {
      address: isProfileLoaded && `https://www.last.fm/user/${viewModel.profileStatistics.username}/loved`
      iconName: 'heart'
      value: isProfileLoaded ? viewModel.profileStatistics.total_loved_tracks : undefined
      caption: 'loved tracks'

      width: parent.width
    }
  }

  // --- User Link ---
  
  // Below profile statistics in code so shadow is on top
  UserLink {
    id: userLink
    
    address: isProfileLoaded ? viewModel.profileStatistics.url : ''
    imageSource: isProfileLoaded ? viewModel.profileStatistics.image_url : ''
    backgroundImageSource: isProfileLoaded ? viewModel.profileStatistics.image_url : ''
    username: isProfileLoaded ? viewModel.profileStatistics.username : ''
    fullName: isProfileLoaded ? viewModel.profileStatistics.real_name : ''

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

  //     top: userStatistics.bottom

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
      top: userStatistics.bottom
      right: parent.right
      bottom: parent.bottom
      left: parent.left

      topMargin: 10
    }

    Flickable {
      id: flickable

      visible: viewModel.isEnabled

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

        // --- Top Artists This Week ---
        
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
              model: viewModel.profileStatistics && viewModel.profileStatistics.top_artists_week

              delegate: ProfileStatistic {
                imageSource: modelData.image_url
                lastfmUrl: modelData.lastfm_url
                title: modelData.title
                plays: modelData.plays
                playsPercentage: modelData.percentage

                width: flickable.width
              }
            }
          }
        }

        // --- Top Artists Overall ---

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
              model: viewModel.profileStatistics && viewModel.profileStatistics.top_artists

              delegate: ProfileStatistic {
                imageSource: modelData.image_url
                lastfmUrl: modelData.lastfm_url
                title: modelData.title
                plays: modelData.plays
                playsPercentage: modelData.percentage

                width: flickable.width
              }
            }
          }
        }

        // // --- Top Albums This Week ---

        // Column {
        //   spacing: 8

        //   width: parent.width

        //   Label {
        //     text: 'Top Albums This Week'
        //     style: kTitleTertiary

        //     x: 15
        //   }

        //   Column {
        //     spacing: 10

        //     width: parent.width

        //     Column {
        //       spacing: 10

        //       width: parent.width

        //       Repeater {
        //         model: viewModel.profileStatistics && viewModel.profileStatistics.top_albums_week

        //         delegate: ProfileStatistic {
        //           imageSource: modelData.image_url
        //           lastfmUrl: modelData.lastfm_url
        //           title: modelData.title
        //           subtitle: modelData.subtitle
        //           secondaryLastfmUrl: modelData.secondary_lastfm_url
        //           plays: modelData.plays
        //           playsPercentage: modelData.percentage

        //           width: flickable.width
        //         }
        //       }
        //     }
        //   }
        // }

        // // --- Top Albums Overall ---

        // Column {
        //   spacing: 8

        //   width: parent.width

        //   Label {
        //     text: 'Top Albums Overall'
        //     style: kTitleTertiary

        //     x: 15
        //   }

        //   Column {
        //     spacing: 10

        //     width: parent.width

        //     Repeater {
        //       model: viewModel.profileStatistics && viewModel.profileStatistics.top_albums

        //       delegate: ProfileStatistic {
        //         imageSource: modelData.image_url
        //         lastfmUrl: modelData.lastfm_url
        //         title: modelData.title
        //         subtitle: modelData.subtitle
        //         secondaryLastfmUrl: modelData.secondary_lastfm_url
        //         plays: modelData.plays
        //         playsPercentage: modelData.percentage

        //         width: flickable.width
        //       }
        //     }
        //   }
        // }

        // // --- Top Tracks This Week ---

        // Column {
        //   spacing: 8

        //   width: parent.width

        //   Label {
        //     text: 'Top Tracks This Week'
        //     style: kTitleTertiary

        //     x: 15
        //   }

        //   Column {
        //     spacing: 10

        //     width: parent.width

        //     Column {
        //       spacing: 10

        //       width: parent.width

        //       Repeater {
        //         model: viewModel.profileStatistics && viewModel.profileStatistics.top_tracks_week

        //         delegate: ProfileStatistic {
        //           imageSource: modelData.image_url
        //           lastfmUrl: modelData.lastfm_url
        //           title: modelData.title
        //           subtitle: modelData.subtitle
        //           secondaryLastfmUrl: modelData.secondary_lastfm_url
        //           plays: modelData.plays
        //           playsPercentage: modelData.percentage

        //           width: flickable.width
        //         }
        //       }
        //     }
        //   }
        // }

        // // --- Top Tracks Overall ---

        // Column {
        //   spacing: 8

        //   width: parent.width

        //   Label {
        //     text: 'Top Tracks Overall'
        //     style: kTitleTertiary

        //     x: 15
        //   }

        //   Column {
        //     spacing: 10

        //     width: parent.width

        //     Repeater {
        //       model: viewModel.profileStatistics && viewModel.profileStatistics.top_tracks

        //       delegate: ProfileStatistic {
        //         imageSource: modelData.image_url
        //         lastfmUrl: modelData.lastfm_url
        //         title: modelData.title
        //         subtitle: modelData.subtitle
        //         secondaryLastfmUrl: modelData.secondary_lastfm_url
        //         plays: modelData.plays
        //         playsPercentage: modelData.percentage

        //         width: flickable.width
        //       }
        //     }
        //   }
        // }
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
