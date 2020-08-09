import QtQuick 2.14
import QtGraphicalEffects 1.0

Image {
  id: root

  width: 33
  height: width

  layer {
    enabled: true

    effect: DropShadow {
      color: Qt.rgba(0, 0, 0, 0.4)
      radius: 3
      verticalOffset: 1
    }
  }

  // Rectangle {
  //   color: '#666'
    
  //   anchors.fill: parent
  // }
}