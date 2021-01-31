import QtQuick 2.14

Rectangle {
  id: bar

  property int index

  radius: width / 2

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
      duration: 175 * (index + 1)
    }

    NumberAnimation {
      target: bar
      property: 'height'
      from: root.topPosition
      to: root.bottomPosition
      duration: 175 * (index + 1)
    }
  }
}