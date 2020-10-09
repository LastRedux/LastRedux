import QtQuick 2.14

Item {
  id: root

  property string iconName
  property bool isLoading
  property bool isSelected

  signal clicked

  opacity: mouseArea.containsPress ? 0.5 : 1

  width: 24
  height: 24

  MouseArea {
    id: mouseArea
    
    onClicked: root.clicked()

    anchors.fill: parent
  }

  Image {
    id: image

    source: `../resources/icons/large/${iconName}${isSelected ? '-active' : ''}.png`

    anchors {
      fill: parent

      margins: -8
    }
  }

  Item {
    id: loadingIndicator

    visible: isLoading && isSelected

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