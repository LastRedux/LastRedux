import QtQuick 2.14
import QtQuick.Controls 2.14

import Kale 1.0

import '../shared/components'

Item {
  id: root

  property ScrobbleHistoryViewModel viewModel

  property bool canDisplayCurrentScrobble: {
    // Don't do just viewModel && viewModel.scrobbleData because we need to return a bool value instead of an undefined viewModel.scrobbleData
    if (viewModel && viewModel.currentScrobbleData) {
      return true
    }

    return false
  }

  // Now scrobbling section
  Column {
    id: nowScrobbling

    spacing: 8

    anchors {
      top: parent.top
      right: parent.right
      left: parent.left

      topMargin: 10
    }

    Button {
      text: 'Play 1st song'

      onClicked: viewModel.MOCK_playSong(0)
    }

    Button {
      text: 'Play 2nd song'

      onClicked: viewModel.MOCK_playSong(1)
    }

    Button {
      text: 'Play 3rd song'

      onClicked: viewModel.MOCK_playSong(2)
    }

    Button {
      text: 'Stop song'

      onClicked: viewModel.MOCK_stopSong()
    }

    Button {
      text: 'Move song to 75%'

      onClicked: viewModel.MOCK_moveTo75Percent()
    }

    Column {
      visible: canDisplayCurrentScrobble
      spacing: 8
      
      width: parent.width

      Item {
        width: parent.width
        height: nowScrobblingTitle.height

        Label {
          id: nowScrobblingTitle

          style: kTitleTertiary
          text: 'Now Scrobbling'

          x: 15
        }

        ScrobbleMeter {
          percentage: viewModel ? viewModel.currentScrobblePercentage : 0

          anchors {
            right: parent.right

            rightMargin: 15

            verticalCenter: parent.verticalCenter
          }
        }
      }

      Scrobble {
        selected: canDisplayCurrentScrobble && viewModel.selectedScrobbleIndex === -1
        name: canDisplayCurrentScrobble && viewModel.currentScrobbleData.name
        artist: canDisplayCurrentScrobble && viewModel.currentScrobbleData.artist
        imageSource: canDisplayCurrentScrobble && viewModel.currentScrobbleData.imageUrl

        // TODO: Add loved attribute

        // Set the selected scrobble index in the view model to -1, which represents the currently selected item in the scrobble history
        onSelect: viewModel.selectedScrobbleIndex = -1
        
        width: parent.width
      }
    }
  }

  // History section
  Item {
    anchors {
      top: nowScrobbling.bottom
      right: parent.right
      bottom: parent.bottom
      left: parent.left

      topMargin: 15
    }

    Label {
      id: historyTitle

      style: kTitleTertiary
      text: 'History'

      x: 15
    }

    ScrobbleHistoryListModel {
      id: listModel

      scrobbleHistoryReference: viewModel
    }

    ListView {
      id: listView

      bottomMargin: 10
      clip: true
      model: listModel

      add: Transition {
        ParallelAnimation {
          NumberAnimation {
            duration: 450
            property: "x"
            from: listView.width * -1
            easing.type: Easing.OutQuint
          }

          NumberAnimation {
            duration: 450
            property: "opacity"
            to: 1
            easing.type: Easing.OutQuint
          }
        }
      }

      addDisplaced: Transition {
        NumberAnimation {
          duration: 450
          properties: "x, y"
          easing.type: Easing.OutQuint
        }
      }

      anchors {
        top: historyTitle.bottom
        right: parent.right
        bottom: parent.bottom
        left: parent.left

        topMargin: 8
      }

      delegate: Scrobble {
        selected: {
          // -2 represents no selection because Qt doesn't understand Python's None value
          if (viewModel && viewModel.selectedScrobbleIndex !== -2) {
            return viewModel.selectedScrobbleIndex === model.index
          }
          
          return false
        }

        name: model.name
        artist: model.artist
        timestamp: model.timestamp
        // imageSource: canDisplayCurrentScrobble && viewModel.currentScrobbleData.album.image_url

        onSelect: viewModel.selectedScrobbleIndex = model.index

        width: listView.width
      }
    }

    WheelScrollArea {
      flickable: listView

      anchors.fill: listView
    }

    Item {
      opacity: listView.contentY - listView.originY > 0

      anchors {
        top: listView.top
        right: parent.right
        left: parent.left
      }

      Behavior on opacity {
        NumberAnimation {
          duration: 450

          easing.type: Easing.OutQuint
        }
      }

      Image {
        fillMode: Image.TileHorizontally
        source: '../shared/resources/effects/tabBarShadow.png'

        width: parent.width
        height: 32
      }

      Rectangle {
        color: '#141414'

        width: parent.width
        height: 1
      }
    }
  }
}
