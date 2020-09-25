import QtQuick 2.14
import QtQuick.Controls 2.14 as Controls

Item {
  property alias isSelected: background.visible
  property string trackTitle
  property string artistName
  property string timestamp
  property alias canLove: heart.isEnabled
  property bool lastfmIsLoved
  property alias imageSource: coverArt.source

  signal select
  signal toggleLastfmIsLoved

  opacity: mouseArea.containsPress ? 0.75 : 1
  
  height: {
    const bottomMargin = 5

    if (timestampLabel.visible) {
      return timestampLabel.y + timestampLabel.height + bottomMargin
    }
    
    return artistNameLabel.y + artistNameLabel.height + bottomMargin
  }

  MouseArea {
    id: mouseArea

    hoverEnabled: true

    onClicked: select()

    anchors.fill: parent
  }

  ScrobbleBackground {
    id: background

    visible: false

    anchors.fill: parent
  }

  // --- Cover Art ---

  Picture {
    id: coverArt

    anchors {
      top: parent.top
      left: parent.left

      topMargin: 5
      leftMargin: 15
    }
  }

  /// --- Track Title ---

  Label {
    id: trackTitleLabel

    // Wrap to 2 lines and then truncate
    elide: Text.ElideRight
    maximumLineCount: 2
    
    style: kTitleSecondary
    text: trackTitle
    wrapMode: Text.Wrap

    anchors {
      top: parent.top
      right: heart.left
      left: coverArt.right

      topMargin: 5
      rightMargin: 5
      leftMargin: 10
    }
  }

  // --- Heart ---

  Heart {
    id: heart

    isActive: lastfmIsLoved

    onClicked: toggleLastfmIsLoved()

    anchors {
      top: parent.top
      right: parent.right

      topMargin: 6
      rightMargin: 15
    }
  }

  // --- Artist Name ---

  Label {
    id: artistNameLabel
    
    // Wrap to 2 lines and then truncate
    elide: Text.ElideRight
    maximumLineCount: 2

    style: kBodyPrimary
    text: artistName
    wrapMode: Text.Wrap

    anchors {
      top: trackTitleLabel.bottom
      right: parent.right
      left: trackTitleLabel.left

      topMargin: 3
      rightMargin: 15
    }
  }

  // --- Timestamp ---

  Label {
    id: timestampLabel

    elide: Text.ElideRight
    style: kTitleTertiary
    text: timestamp
    visible: timestamp

    anchors {
      top: artistNameLabel.bottom
      right: parent.right
      left: trackTitleLabel.left

      topMargin: 3
      rightMargin: 15
    }
  }
}
