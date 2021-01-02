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
      isLoading: model.isLoading
      isContextMenuEnabled: !viewModel.isLoading // Prevent crash by disabling context menu when the list view is about to be refreshed
      z: listView.count - model.index // Topmost items should appear highest in the z stack so shadows are not covered by subsequent items

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
      visible: viewModel.isEnabled

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