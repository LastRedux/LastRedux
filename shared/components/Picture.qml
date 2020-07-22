import QtQuick 2.15
import QtGraphicalEffects 1.0

Rectangle {
  color: '#666'

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
}