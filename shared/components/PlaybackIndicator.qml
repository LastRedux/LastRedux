import QtQuick 2.14

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

      x: (isLarge ? 7 : 4) * (model.index + 1)
      y: isLarge ? 7 + (17 - height) : 4 + (10 - height)
      width: isLarge ? 3 : 2

      Rectangle {
        color: Qt.rgba(0, 0, 0, 0.25)
        radius: width / 2
        z: -1

        y: -1
        width: parent.width
        height: width
      }

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