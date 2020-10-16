import QtQuick 2.14

import "../../shared/components"

Item {
  property bool hasImage: true
  property alias imageSource: picture.source
  property alias lastfmUrl: titleLink.address
  property alias title: titleLink.text
  property alias subtitle: subtitleLabel.text
  property string scrobbleCount
  property alias scrobbleCountPercentage: scrobbleCountProgressBar.percentage

  height: Math.max(picture.height, scrobbleCountLabel.y + scrobbleCountLabel.height)

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

  Link {
    id: titleLink

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

    y: titleLink.y + titleLink.height + 1

    anchors {
      right: titleLink.right
      left: titleLink.left
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

      return titleLink.y + titleLink.height + topMargin
    }

    anchors {
      right: scrobbleCountLabel.left
      left: titleLink.left

      rightMargin: hasImage ? 8 : 15
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

      right: titleLink.right
    }
  }
}