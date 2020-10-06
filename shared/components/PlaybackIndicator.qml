import QtQuick 2.14
import QtGraphicalEffects 1.12

Item {
  id: root
  
  property bool isLarge: false

  width: isLarge ? 31 : 18
  height: isLarge ? 31 : 18

  Image {
    source: `../resources/playbackIndicatorBackground${isLarge ? '-large' : ''}.png`

    anchors {
      fill: parent

      margins: -6
    }
  }

  Repeater {
    model: 3
  
    delegate: Rectangle {
      id: bar

      radius: width / 2

      layer {
        enabled: root.visible

        effect: DropShadow {
          color: Qt.rgba(0, 0, 0, 0.25)
          radius: 0
          verticalOffset: -1
        }
      }

      x: (isLarge ? 7 : 4) * (model.index + 1)
      y: isLarge ? 7 + (17 - height) : 4 + (10 - height)
      width: isLarge ? 3 : 2

      SequentialAnimation {
        loops: Animation.Infinite
        running: root.visible

        NumberAnimation {
          target: bar
          property: 'height'
          to: isLarge ? 17 : 10
          duration: 175 * (model.index + 1)
        }

        NumberAnimation {
          target: bar
          property: 'height'
          to: isLarge ? 3 : 2
          duration: 175 * (model.index + 1)
        }
      }
    }
  }
}