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
  
  height: column.y + column.height + 5

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

  Column {
    id: column

    spacing: 3

    anchors {
      top: trackTitleLabel.bottom
      right: parent.right
      left: trackTitleLabel.left

      topMargin: 3
      rightMargin: 15
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

      width: parent.width
    }

    // --- Timestamp ---

    Label {
      id: timestampLabel

      elide: Text.ElideRight
      style: kTitleTertiary
      text: timestamp
      visible: timestamp
    }
  }
}
