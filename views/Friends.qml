import QtQuick 2.14

import Kale 1.0

import '../shared/components'
// import 'Friends'

Item {
  id: root

  property FriendsViewModel viewModel

  FriendsListModel {
    id: listModel

    friendsReference: viewModel
  }
  
  Component.onCompleted: {
    if (viewModel) {
      viewModel.loadFriends()
    }
  }

  Label {
    visible: listView.count === 0
    text: 'Loading...'
  }

  ListView {
    id: listView

    model: listModel

    clip: true // Prevent content from appearing outside the list's bounding box

    anchors.fill: parent

    delegate: Column {
      width: listView.width
      spacing: 5

      Label {
        text: model.username
      }

      Label {
        text: model.realName
      }

      Label {
        text: model.currentTrackTitle
      }

      Label {
        text: model.currentTrackArtistName
      }

      Rectangle {
        width: 10
        height: 10
        
        color: model.currentTrackIsPlaying ? 'blue' : 'gray'
      }
    }
  }
}