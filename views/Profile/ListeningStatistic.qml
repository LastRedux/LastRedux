import QtQuick 2.14

import "../../shared/components"

Item {
  property bool hasImage: true
  property alias imageSource: picture.source
  property string lastfmUrl
  property alias title: titleLabel.text
  property alias subtitle: subtitleLabel.text
  property string scrobbleCount
  property alias scrobbleCountPercentage: scrobbleCountProgressBar.percentage

  opacity: hoverHandler.hovered && pointHandler.active ? 0.5 : 1

  height: Math.max(picture.height, scrobbleCountLabel.y + scrobbleCountLabel.height)

  // --- Pointer Handlers ---

  HoverHandler {
    id: hoverHandler
  }

  // TODO: Add context menu
  PointHandler {
    id: pointHandler

    enabled: !!lastfmUrl
  }
  
  TapHandler {
    acceptedButtons: Qt.LeftButton

    onTapped: {
      if (lastfmUrl) {
        console.log(lastfmUrl)
        Qt.openUrlExternally(lastfmUrl)
      }
    }
  }

  // --- Picture ---

  Picture {
    id: picture

    type: kArtist // TODO: Allow configuration
    visible: hasImage

    anchors {
      top: parent.top
      left: parent.left

      leftMargin: 15
    }
  }

  /// --- Title ---

  Label {
    id: titleLabel

    elide: Text.ElideRight
    maximumLineCount: 2

    style: kTitleSecondary
    wrapMode: Text.Wrap

    y: 2

    anchors {
      right: parent.right
      left: hasImage ? picture.right : parent.left

      rightMargin: 15
      leftMargin: hasImage ? 10 : 15
    }
  }

  // --- Subtitle ---

  Label {
    id: subtitleLabel
    
    elide: Text.ElideRight
    maximumLineCount: 2
    visible: text
    wrapMode: Text.Wrap

    y: titleLabel.y + titleLabel.height + 1

    anchors {
      right: titleLabel.right
      left: titleLabel.left
    }
  }

  // --- Scrobble Count ---

  ProgressBar {
    id: scrobbleCountProgressBar

    percentage: 1

    y: {
      let topMargin = 6

      if (subtitleLabel.visible) {
        return subtitleLabel.y + subtitleLabel.height + topMargin
      }

      return titleLabel.y + titleLabel.height + topMargin
    }

    anchors {
      right: scrobbleCountLabel.left
      left: titleLabel.left

      rightMargin: 8
    }
  }

  Label {
    id: scrobbleCountLabel

    horizontalAlignment: Qt.AlignRight
    style: kTitleTertiary
    text: `${scrobbleCount} plays`

    width: 62

    anchors {
      verticalCenter: scrobbleCountProgressBar.verticalCenter

      right: titleLabel.right
    }
  }
}