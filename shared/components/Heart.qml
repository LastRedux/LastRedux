import QtQuick 2.14

Item {
  id: root

  property bool isActive
  property bool isEnabled: true

  signal clicked

  opacity: !isEnabled || mouseArea.containsPress ? 0.5 : 1

  width: 14
  height: 13

  Image {
    source: `../resources/heart${isActive ? '-active' : ''}.png`

    anchors {
      fill: parent

      topMargin: -2
      rightMargin: -3
      bottomMargin: -4
      leftMargin: -3
    }
  }

  MouseArea {
    id: mouseArea

    onClicked: {
      root.clicked()
    }
    
    anchors.fill: parent
  }
}