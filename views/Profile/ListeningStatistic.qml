import QtQuick 2.14

import "../../shared/components"

Item {
  property bool hasImage: true
  property alias imageSource: picture.source
  property alias lastfmUrl: titleLink.address
  property var secondaryLastfmUrl
  property alias title: titleLink.text
  property alias subtitle: subtitleLink.text
  property string plays
  property alias playsPercentage: playsProgressBar.percentage

  height: Math.max(picture.height, playsLabel.y + playsLabel.height)

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

  Link {
    id: subtitleLink
    
    elide: Text.ElideRight
    maximumLineCount: 2
    visible: text
    wrapMode: Text.Wrap
    style: kBodyPrimary
    
    address: secondaryLastfmUrl || null

    y: titleLink.y + titleLink.height + 1

    anchors {
      right: titleLink.right
      left: titleLink.left
    }
  }

  // --- Scrobble Count ---

  ProgressBar {
    id: playsProgressBar

    percentage: 1

    y: {
      let topMargin = 6

      if (subtitleLink.visible) {
        return subtitleLink.y + subtitleLink.height + topMargin
      }

      return titleLink.y + titleLink.height + topMargin
    }

    anchors {
      right: playsLabel.left
      left: titleLink.left

      rightMargin: hasImage ? 8 : 15
    }
  }

  Label {
    id: playsLabel

    horizontalAlignment: Qt.AlignRight
    style: kTitleTertiary
    text: `${plays} plays`

    width: 62

    anchors {
      verticalCenter: playsProgressBar.verticalCenter

      right: titleLink.right
    }
  }
}