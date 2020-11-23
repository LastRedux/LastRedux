import QtQuick 2.15
import QtGraphicalEffects 1.12

import '../../shared/components'

Item {
  id: root

  property var userLastfmUrl
  property alias userImage: userImageView.source
  property string username
  property string userRealName

  property string trackImage
  property var trackTitle
  property var trackArtistName
  property alias trackLastfmUrl: trackTitleLabel.address
  property alias trackArtistLastfmUrl: trackArtistNameView.address
  property bool isTrackPlaying
  property bool hasAdditionalData

  property bool shouldShowTrackSection: !hasAdditionalData || (hasAdditionalData && trackTitle)

  height: shouldShowTrackSection ? trackLink.y + trackLink.height : userLink.height

  Picture {
    source: trackImage || ''
    visible: isTrackPlaying

    anchors.fill: parent

    LinearGradient {
      anchors.fill: parent

      gradient: Gradient {
        GradientStop {
          color: Qt.rgba(0, 0, 0, 0.5)
          position: 0
        }

        GradientStop {
          color: Qt.rgba(0, 0, 0, 0.75)
          position: 1
        }
      }
    }

    // --- Shadow and Border ---

    Image {
      fillMode: Image.TileHorizontally
      source: '../../shared/resources/effects/trackDetailsShadow.png'

      height: 16

      // Position outside of and under bounding box
      anchors {
        top: parent.bottom
        right: parent.right
        left: parent.left
      }
    }

    Rectangle {
      color: Qt.rgba(0, 0, 0, 0.23)

      height: 1

      anchors {
        top: parent.bottom
        right: parent.right
        left: parent.left
      }
    }
  }

  Item {
    id: userLink

    opacity: pointerHandlers.containsPress ? 0.5 : 1

    width: parent.width
    height: userImageView.height + 20

    // --- User Link Pointer Handlers ---

    LinkPointerHandlers {
      id: pointerHandlers

      address: userLastfmUrl

      text: {
        if (root.userRealName) {
          return `${root.username} (${root.userRealName})`
        }

        return root.username
      }

      anchors.fill: parent
    }

    // --- User Image ---

    Picture {
      id: userImageView

      type: kUser

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
        isShadowEnabled: !isTrackPlaying
        text: root.username
        style: kTitleSecondary

        width: parent.width
      }

      Label {
        id: userRealNameLabel

        color: Qt.rgba(1, 1, 1, 0.81)
        elide: Text.ElideRight
        isShadowEnabled: !isTrackPlaying
        text: root.userRealName
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

    visible: shouldShowTrackSection
    
    y: userLink.height
    width: parent.width
    height: shouldShowTrackSection ? trackArtistNameView.y + trackArtistNameView.height + 10 : 0

    // --- Track Playback Status - Not Currently Playing ---

    Item {
      id: notCurrentlyPlaying

      visible: !isTrackPlaying

      width: 18
      height: 18

      anchors {
        top: parent.top
        left: parent.left

        leftMargin: 15
      }

      Image {
        source: `../../shared/resources/icons/small/clock.png`

        anchors {
          fill: parent

          margins: -6
        }
      }
    }

    // --- Track Playback Status - Currently Playing ---

    PlaybackIndicator {
      id: playbackIndicator

      visible: isTrackPlaying

      anchors {
        top: parent.top
        left: parent.left

        leftMargin: 15
      }
    }

    // --- Track Title ---

    Link {
      id: trackTitleLabel

      elide: Text.ElideRight
      maximumLineCount: 2
      isShadowEnabled: !isTrackPlaying
      text: trackTitle
      wrapMode: Text.Wrap
      visible: hasAdditionalData

      anchors {
        top: parent.top
        right: parent.right
        left: playbackIndicator.right

        rightMargin: 15
        leftMargin: 10
      }
    }

    Placeholder {
      id: trackTitlePlaceholder

      visible: !hasAdditionalData

      width: 60 + Math.ceil(Math.random() * 70)

      anchors {
        top: trackTitleLabel.top
        left: trackTitleLabel.left
      }
    }

    // --- Track Artist Name ---

    Link {
      id: trackArtistNameView

      elide: Text.ElideRight
      maximumLineCount: 2
      isShadowEnabled: !isTrackPlaying
      opacity: 0.81
      style: kBodyPrimary
      text: trackArtistName
      wrapMode: Text.Wrap
      visible: hasAdditionalData

      anchors {
        top: trackTitleLabel.bottom
        right: trackTitleLabel.right
        left: trackTitleLabel.left

        topMargin: 1
      }
    }

    Placeholder {
      visible: !hasAdditionalData
      
      width: 40 + Math.ceil(Math.random() * 70)

      anchors {
        top: trackTitlePlaceholder.bottom
        left: trackTitleLabel.left

        topMargin: 1
      }
    }
  }
}