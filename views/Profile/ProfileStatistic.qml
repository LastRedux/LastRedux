import QtQuick 2.14

import '../../shared/components'

Item {
  property string iconName
  property alias text: label.text
  
  height: iconContainer.height

  Item {
    id: iconContainer

    width: 18
    height: width

    Image {
      source: `../../shared/resources/icons/small/${iconName}.png`

      anchors.centerIn: parent
    }

    anchors {
      top: parent.top
      left: parent.left
    }
  }

  Label {
    id: label
    
    elide: Text.ElideRight
    style: kCaption

    anchors {
      verticalCenter: iconContainer.verticalCenter

      right: parent.right
      left: iconContainer.right

      leftMargin: 10
    }
  }
}