import QtQuick 2.14

Item {
  id: root

  property int bottomPosition: isLarge ? 3 : 2
  property int topPosition: isLarge ? 17 : 10
  
  property bool isLarge: false
  property bool isPaused: false

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

      property int cachedIndex: 0

      radius: width / 2

      x: (isLarge ? 7 : 4) * (model.index + 1)
      y: isLarge ? 7 + (17 - height) : 4 + (10 - height)
      width: isLarge ? 3 : 2

      Component.onCompleted: {
        cachedIndex = model.index
      }

      Rectangle {
        color: Qt.rgba(0, 0, 0, 0.25)
        radius: width / 2
        z: -1

        y: -1
        width: parent.width
        height: width
      }

      states: State {
        name: 'paused'
        when: !root.visible || root.isPaused

        PropertyChanges {
          target: animation
          running: false
        }
      }

      transitions: Transition {
        from: ''
        to: 'paused'

        NumberAnimation {
          target: bar
          property: 'height'
          to: width
          duration: bar.height * 10
        }
      }

      SequentialAnimation {
        id: animation

        loops: Animation.Infinite
        running: true

        NumberAnimation {
          target: bar
          property: 'height'
          from: root.bottomPosition
          to: root.topPosition
          duration: 175 * (cachedIndex + 1)
        }

        NumberAnimation {
          target: bar
          property: 'height'
          from: root.topPosition
          to: root.bottomPosition
          duration: 175 * (cachedIndex + 1)
        }
      }
    }
  }
}