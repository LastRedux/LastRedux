import QtQuick 2.14

import '../../shared/components'

Item {
  id: root

  property var userAddress
  property alias userImage: userImageView.source
  property alias username: usernameLabel.text
  property alias userRealName: userRealNameLabel.text

  property string trackTitle
  property string trackArtistName
  property bool isTrackPlaying

  opacity: userLinkHoverHandler.hovered && userLinkPointHandler.active ? 0.5 : 1

  height: trackTitle ? trackLink.y + trackLink.height : userLink.height

  Item {
    id: userLink

    width: parent.width
    height: userImageView.height + 20

    // --- User Link Handlers ---

    HoverHandler {
      id: userLinkHoverHandler
    }

    PointHandler {
      id: userLinkPointHandler

      enabled: !!userAddress
    }

    TapHandler {
      acceptedButtons: Qt.LeftButton

      onTapped: {
        if (userAddress) {
          Qt.openUrlExternally(userAddress)
        }
      }
    }

    // --- User Image ---

    Picture {
      id: userImageView

      type: kArtist // TODO: Add user type

      anchors {
        top: parent.top
        left: parent.left

        topMargin: 10
        leftMargin: 15
      }
    }

    Column {
      spacing: 2

      anchors {
        verticalCenter: parent.verticalCenter

        right: externalLinkIcon.left
        left: userImageView.right

        rightMargin: 10
        leftMargin: 10
      }

      // --- User Name ---

      Label {
        id: usernameLabel

        elide: Text.ElideRight
        style: kTitleSecondary

        width: parent.width
      }

      Label {
        id: userRealNameLabel

        elide: Text.ElideRight
        opacity: 0.81
        visible: text

        width: parent.width
      }
    }

    // --- External Link Icon ---

    Image {
      id: externalLinkIcon

      source: '../../shared/resources/externalLink.png'

      anchors {
        verticalCenter: parent.verticalCenter

        right: parent.right

        rightMargin: 15
      }
    }
  }

  Item {
    id: trackLink

    visible: trackTitle
    
    y: userLink.height
    width: parent.width
    height: trackTitle ? trackArtistNameView.y + trackArtistNameView.height + 10 : 0

    // --- Track Playback Status ---

    Rectangle {
      id: trackPlaybackStatusView

      color: isTrackPlaying ? 'cyan' : 'gray'
      radius: 5

      width: 18
      height: 18

      anchors {
        top: parent.top
        left: parent.left

        leftMargin: 15
      }
    }

    // --- Track Title ---

    Label {
      id: trackTitleLabel

      elide: Text.ElideRight
      style: kTitleSecondary
      text: trackTitle || ''

      anchors {
        top: parent.top
        right: parent.right
        left: trackPlaybackStatusView.right

        rightMargin: 15
        leftMargin: 10
      }
    }

    // --- Track Artist Name ---

    Label {
      id: trackArtistNameView

      elide: Text.ElideRight
      opacity: 0.81
      text: trackArtistName || ''

      anchors {
        top: trackTitleLabel.bottom
        right: trackTitleLabel.right
        left: trackTitleLabel.left

        topMargin: 1
      }
    }
  }
}