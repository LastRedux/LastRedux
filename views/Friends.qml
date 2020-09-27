import QtQuick 2.14

import Kale 1.0

import '../shared/components'
import 'Friends'

Item {
  id: root

  property FriendsListModel listModel
  property FriendsViewModel viewModel

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

    clip: true // Prevent content from appearing outside the list's bounding box
    model: listModel

    anchors.fill: parent

    delegate: Friend {
      userAddress: model.lastfmUrl
      userImage: model.imageUrl
      username: model.username
      userRealName: model.realName
      trackTitle: model.currentTrackTitle
      trackArtistName: model.currentTrackArtistName
      isTrackPlaying: model.isCurrentTrackPlaying

      width: listView.width
    }
  }
}