import QtQuick 2.14

import Kale 1.0

import '../shared/components'

Item {
  property ScrobbleDetailsViewModel viewModel

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
          text: viewModel && viewModel.track

          width: parent.width
        }

        Link {
          elide: Text.ElideRight
          text: viewModel && viewModel.artist

          width: parent.width
        }

        Row {
          spacing: 3
          
          Label {
            style: kBodyPrimary
            text: 'from'
          }

          Link {
            text: viewModel && viewModel.album
          }
        }
      }

      Label {
        style: kTitleTertiary
        text: '## plays'
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

    Picture {
      id: artistAvatar

      width: 106

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
        text: viewModel && viewModel.artist

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
