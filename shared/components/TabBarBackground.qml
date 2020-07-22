import QtQuick 2.15

Image {
  fillMode: Image.TileHorizontally
  source: '../resources/effects/tabBarGradient.png'

  height: 22 + 44

  // Shadow
  Image {
    fillMode: Image.TileHorizontally
    source: '../resources/effects/tabBarShadow.png'

    height: 32

    anchors {
      top: parent.bottom
      right: parent.right
      left: parent.left
    }
  }

  // Border
  Rectangle {
    color: '#141414'

    height: 1

    anchors {
      top: parent.bottom
      right: parent.right
      left: parent.left
    }
  }
}
