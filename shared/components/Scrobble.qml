import QtQuick 2.14

Item {
  property alias isSelected: background.visible
  property string trackTitle: '???'
  property string artistName: '???'
  property string timestamp
  property alias imageSource: coverArt.source

  signal select

  opacity: mouseArea.containsPress ? 0.75 : 1
  
  height: details.height + 10

  ScrobbleBackground {
    id: background

    visible: false

    anchors.fill: parent
  }

  Picture {
    id: coverArt

    anchors {
      top: parent.top
      left: parent.left

      topMargin: 5
      leftMargin: 15
    }
  }

  Column {
    id: details

    spacing: 3

    anchors {
      top: parent.top
      right: parent.right
      left: coverArt.right

      topMargin: 5
      rightMargin: 15
      leftMargin: 10
    }

    Label {
      // Wrap to 2 lines and then truncate
      elide: Text.ElideRight
      maximumLineCount: 2
      
      style: kTitleSecondary
      text: trackTitle
      wrapMode: Text.Wrap

      width: parent.width
    }

    Label {
      // Wrap to 2 lines and then truncate
      elide: Text.ElideRight
      maximumLineCount: 2

      style: kBodyPrimary
      text: artistName
      wrapMode: Text.Wrap

      width: parent.width
    }

    Label {
      elide: Text.ElideRight
      style: kTitleTertiary
      text: timestamp
      visible: timestamp

      width: parent.width
    }
  }

  MouseArea {
    id: mouseArea

    hoverEnabled: true

    onClicked: select()

    anchors.fill: parent
  }
}
