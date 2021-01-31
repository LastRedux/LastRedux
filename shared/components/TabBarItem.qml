import QtQuick 2.14

ToolbarItem {
  property bool isLoading

  onIsLoadingChanged: {
    if (isLoading) {
      sequentialAnimation.restart()
    }
  }

  states: [
    State {
      name: ''
      when: !isLoading

      PropertyChanges {
        target: loadingIndicator
        fadeOpacity: 0
      }
    },
    State {
      name: 'loading'
      when: isLoading

      PropertyChanges {
        target: loadingIndicator
        fadeOpacity: 1
      }
    }
  ]

  transitions: Transition {
    from: 'loading'
    to: ''

    NumberAnimation {
      target: loadingIndicator
      property: 'fadeOpacity'
      duration: 450
    }
  }

  Item {
    id: loadingIndicator

    property real animatedOpacity: 0
    property real fadeOpacity: 1

    opacity: animatedOpacity * fadeOpacity

    width: 5
    height: width

    anchors {
      horizontalCenter: parent.horizontalCenter

      bottom: parent.bottom

      bottomMargin: -6
    }

    Image {
      source: '../resources/loadingIndicator.png'

      anchors {
        fill: parent

        margins: -16
      }
    }

    SequentialAnimation {
      id: sequentialAnimation

      loops: Animation.Infinite

      NumberAnimation {
        target: loadingIndicator
        property: 'animatedOpacity'
        from: 0
        to: 1
        duration: 450
      }

      NumberAnimation {
        target: loadingIndicator
        property: 'animatedOpacity'
        from: 1
        to: 0
        duration: 450
      }
    }
  }
}