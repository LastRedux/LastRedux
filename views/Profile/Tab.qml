import QtQuick 2.14

import "../../shared/components"

Item {
  id: root
  
  property alias title: label.text
  property bool isSelected

  signal clicked

  opacity: mouseArea.containsPress ? 0.5 : 1

  width: 20 + label.width
  height: 20

  MouseArea {
    id: mouseArea

    hoverEnabled: true

    onClicked: root.clicked()

    anchors.fill: parent
  }

  Rectangle {
    id: background
    
    color: Qt.rgba(1, 1, 1, 0.2)
    radius: height / 2
    visible: isSelected || mouseArea.containsMouse

    anchors.fill: parent
  }

  Label {
    id: label

    isShadowEnabled: !isSelected
    style: kCaption
    verticalAlignment: Qt.AlignVCenter

    x: 10
    height: parent.height
  }
}