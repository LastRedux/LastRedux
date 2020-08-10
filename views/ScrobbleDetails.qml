import QtQuick 2.14

import Kale 1.0

import '../shared/components'

Item {
  property ScrobbleDetailsViewModel viewModel

  property bool canDisplayScrobble: {
    // Don't do just viewModel && viewModel.scrobbleData because we need to return a bool value instead of an undefined viewModel.scrobbleData
    if (viewModel && viewModel.scrobbleData) {
      return true
    }

    return false
  }

  // No song playing page
  Item {
    visible: !canDisplayScrobble

    anchors.fill: parent

    Label {
      opacity: 0.5
      style: kTitleSecondary
      
      text: 'No Scrobble Selected'

      anchors.centerIn: parent
    }
  }

  // Song info page
  Item {
    visible: canDisplayScrobble

    anchors.fill: parent
    
    // Song details
    Rectangle {
      id: songDetails
      
      color: '#111'

      height: coverArt.height + 30 * 2

      anchors {
        top: parent.top
        right: parent.right
        left: parent.left
      }

      Picture {
        id: coverArt

        source: {
          if (canDisplayScrobble && viewModel.scrobbleData.is_additional_data_downloaded) {
            return viewModel.scrobbleData.album.image_url
          }
          
          return ''
        }

        width: 160

        anchors {
          top: parent.top
          left: parent.left

          margins: 30
        }
      }

      Column {
        spacing: 10

        anchors {
          top: coverArt.top
          right: parent.right
          left: coverArt.right

          topMargin: 10
          rightMargin: 30
          leftMargin: 20
        }

        Column {
          spacing: 5

          width: parent.width

          Link {
            elide: Text.ElideRight
            style: kTitlePrimary
            text: canDisplayScrobble && viewModel.scrobbleData.name

            width: parent.width
          }

          Link {
            elide: Text.ElideRight
            text: canDisplayScrobble && viewModel.scrobbleData.artist.name

            width: parent.width
          }

          Row {
            spacing: 3
            
            Label {
              style: kBodyPrimary
              text: 'from'
            }

            Link {
              text: canDisplayScrobble && viewModel.scrobbleData.album.name
            }
          }
        }

        Label {
          style: kTitleTertiary
          visible: canDisplayScrobble && viewModel.scrobbleData.is_additional_data_downloaded

          text: {
            if (canDisplayScrobble) {
              if (viewModel.scrobbleData.is_additional_data_downloaded) {
                const playCount = viewModel.scrobbleData.plays

                if (playCount === 1) {
                  return '1 play'
                } else {
                  return `${playCount} plays`
                }
              }
            }

            return ''
          }
        }
      }
    }

    // Artist details
    Item {
      id: artistDetails

      anchors {
        top: songDetails.bottom
        right: parent.right
        left: parent.left
      }

      Rectangle {
        id: artistAvatar

        opacity: 0.1

        width: 106
        height: width

        anchors {
          top: parent.top
          left: parent.left

          margins: 30
        }
      }

      Column {
        spacing: 15

        anchors {
          top: artistAvatar.top
          right: parent.right
          left: artistAvatar.right

          topMargin: 10
          rightMargin: 30
          leftMargin: 20
        }

        Link {
          elide: Text.ElideRight
          style: kTitlePrimary
          text: canDisplayScrobble && viewModel.scrobbleData.artist.name

          width: parent.width
        }

        Row {
          id: row

          property int columnSpacing: 3

          spacing: 20

          Column {
            spacing: row.columnSpacing

            Label {
              style: kNumber
              text: '###'
            }

            Label {
              style: kTitleTertiary
              text: 'Listeners'
            }
          }

          Column {
            spacing: row.columnSpacing
            
            Label {
              style: kNumber
              text: '###'
            }

            Label {
              style: kTitleTertiary
              text: 'Plays'
            }
          }

          Column {
            spacing: row.columnSpacing
            
            Label {
              style: kNumber
              text: '###'
            }

            Label {
              style: kTitleTertiary
              text: 'Plays in Library'
            }
          }
        }

        Column {
          spacing: 5

          width: parent.width
          
          // TODO: Move styles for selectable text to component
          TextEdit {
            id: textEdit

            color: '#FFF'
            readOnly: true
            renderType: Text.NativeRendering
            selectByMouse: true
            selectionColor: Qt.rgba(255, 255, 255, 0.15)
            text: 'Artist Bio'
            wrapMode: Text.Wrap

            font {
              letterSpacing: 0.25
              weight: Font.Medium
            }

            width: parent.width

            TextContextMenu {
              text: textEdit

              anchors.fill: parent
            }
          }

          Link {
            text: 'Read more on Last.fm'
          }
        }
      }
    }
  }
}
