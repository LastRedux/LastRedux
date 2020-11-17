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
      z: listView.count - model.index // Topmost items should appear highest in the z stack so shadows are not covered by subsequent items

      width: listView.width
    }
  }

  WheelScrollArea {
    flickable: listView
    
    anchors.fill: listView
  }
}