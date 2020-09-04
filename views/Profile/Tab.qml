import QtQuick 2.14

import "../../shared/components"

Item {
  property alias title: label.text
  property bool isSelected

  width: 20 + label.width
  height: 20

  Rectangle {
    id: background
    
    color: Qt.rgba(1, 1, 1, 0.2)
    radius: height / 2
    visible: isSelected

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