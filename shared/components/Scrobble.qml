import QtQuick 2.14

Item {
  property alias selected: background.visible
  property string track: '???'
  property string artist: '???'
  property string timestamp

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

    spacing: 1

    anchors {
      top: parent.top
      right: parent.right
      left: coverArt.right

      topMargin: 5
      rightMargin: 15
      leftMargin: 10
    }

    Label {
      elide: Text.ElideRight
      maximumLineCount: 2
      style: kTitleSecondary
      text: track
      wrapMode: Text.Wrap

      width: parent.width
    }

    Label {
      elide: Text.ElideRight
      maximumLineCount: 2
      style: kBodyPrimary
      text: artist
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
