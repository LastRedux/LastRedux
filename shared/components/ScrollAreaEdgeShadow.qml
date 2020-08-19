import QtQuick 2.14

Item {
  Behavior on opacity {
    NumberAnimation {
      duration: 450

      easing.type: Easing.OutQuint
    }
  }

  // --- Shadow ---

  Image {
    fillMode: Image.TileHorizontally
    source: '../resources/effects/tabBarShadow.png'

    width: parent.width
    height: 32
  }

  // --- Border ---

  Rectangle {
    color: '#141414'

    width: parent.width
    height: 1
  }
}
