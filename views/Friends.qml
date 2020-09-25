import QtQuick 2.14

import Kale 1.0

import '../shared/components'
// import 'Friends'

Item {
  id: root

  property FriendsViewModel viewModel

  Component.onCompleted: {
    if (viewModel) {
      viewModel.loadFriends()
    }
  }

  Column {
    spacing: 10

    Label {
      visible: viewModel && viewModel.friendsArray.length

      text: 'Loading...'
    }

    Repeater {
      model: viewModel.friendsArray
      visible: !!viewModel.friendsArray

      delegate: Column {
        spacing: 5

        Label {
          text: modelData.username
        }

        Label {
          text: modelData.real_name
        }

        Label {
          text: modelData.current_track.title
        }

        Label {
          text: modelData.current_track.artist.name
        }

        Rectangle {
          width: 10
          height: 10
          
          color: modelData.is_current_track_playing ? 'blue' : 'gray'
        }
      }
    }
  }
}