import QtQuick 2.14

ToolbarItem {
  property bool shouldShowLoadingIndicator

  Item {
    id: loadingIndicator

    visible: shouldShowLoadingIndicator

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
      loops: Animation.Infinite
      running: loadingIndicator

      NumberAnimation {
        target: loadingIndicator
        property: 'opacity'
        to: 1
        duration: 450
      }

      NumberAnimation {
        target: loadingIndicator
        property: 'opacity'
        to: 0
        duration: 450
      }
    }
  }
}