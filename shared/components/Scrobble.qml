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

    x: 15
    y: 5
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

    x: coverArt.x + coverArt.width + 10
    y: 5
    width: parent.width - x - 15 - heart.width - 10
  }

  // --- Heart ---

  Heart {
    id: heart

    isActive: lastfmIsLoved

    onClicked: canLove && toggleLastfmIsLoved()

    y: 6
    x: parent.width - 15 - width
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

    x: trackTitleLabel.x
    y: trackTitleLabel.y + trackTitleLabel.height + 3
    width: parent.width - x - 15
  }

  // --- Timestamp ---

  Label {
    id: timestampLabel

    elide: Text.ElideRight
    style: kTitleTertiary
    text: timestamp
    visible: timestamp

    x: trackTitleLabel.x
    y: artistNameLabel.y + artistNameLabel.height + 3
    width: artistNameLabel.width
  }
}
