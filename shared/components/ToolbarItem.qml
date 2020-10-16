import QtQuick 2.14

Item {
  id: root

  property string iconName
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
}