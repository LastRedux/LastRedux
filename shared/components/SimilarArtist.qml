import QtQuick 2.14

Item {
  property alias name: link.text
  property alias imageSource: picture.source
  property alias lastfmUrl: link.address

  height: picture.height

  Picture {
    id: picture
  }

  Link {
    id: link

    // Wrap to 2 lines and then truncate
    maximumLineCount: 2
    elide: Text.ElideRight

    anchors {
      verticalCenter: parent.verticalCenter

      right: parent.right
      left: picture.right

      leftMargin: 15
    }
  }
}