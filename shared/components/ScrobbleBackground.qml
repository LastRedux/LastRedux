import QtQuick 2.14

Image {
  fillMode: Image.TileHorizontally
  source: '../resources/effects/scrobbleGradient.png'

  // Inner Highlight
  Rectangle {
    color: '#595959'

    height: 1

    anchors {
      top: parent.top
      right: parent.right
      left: parent.left
    }
  }

  // Inner Shadow
  Rectangle {
    color: '#191919'

    height: 1

    anchors {
      right: parent.right
      bottom: parent.bottom
      left: parent.left
    }
  }
}
