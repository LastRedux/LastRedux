import QtQuick 2.14

import Kale 1.0

import '../shared/components'
import 'Friends'

Item {
  id: root

  property FriendsListModel listModel
  property FriendsViewModel viewModel

  ListView {
    id: listView
    visible: count > 0

    clip: true // Prevent content from appearing outside the list's bounding box
    model: listModel

    anchors.fill: parent

    delegate: Friend {
      userLastfmUrl: model.lastfmUrl
      userImage: model.imageUrl
      username: model.username
      userRealName: model.realName
      trackTitle: model.trackTitle
      trackImage: model.trackAlbumImageUrl
      trackLastfmUrl: model.trackLastfmUrl
      trackArtistName: model.trackArtistName
      trackArtistLastfmUrl: model.trackArtistLastfmUrl
      isTrackPlaying: model.isTrackPlaying

      width: listView.width
    }
  }

  Item {
    visible: listView.count == 0 && !viewModel.shouldShowLoadingIndicator

    anchors.fill: parent

    Label {
      opacity: 0.5
      
      text: 'You haven\'t added any friends on Last.fm yet.'
      wrapMode: Text.Wrap
      horizontalAlignment: Qt.AlignHCenter

      anchors {
        verticalCenter: parent.verticalCenter
        
        left: parent.left
        right: parent.right

        margins: 24
      }
    }
  }

  WheelScrollArea {
    flickable: listView
    
    anchors.fill: listView
  }
}