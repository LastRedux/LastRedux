import QtQuick 2.14

import '../../shared/components'
import '../../util/helpers.js' as Helpers

Item {
  property string iconName
  property var value
  property string caption
  
  height: iconContainer.height

  // --- Icon ---

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

  // --- Value and Caption ---

  Label {
    id: label
    
    elide: Text.ElideRight
    style: kCaption
    text: value ? `${Helpers.numberWithCommas(value)} ${caption}` : caption
    visible: value

    anchors {
      verticalCenter: iconContainer.verticalCenter

      right: parent.right
      left: iconContainer.right

      leftMargin: 10
    }
  }

  // --- Placeholder Box ---

  Rectangle {
    opacity: 0.2
    radius: 4
    visible: !value

    width: label.contentWidth + 15
    height: 16

    anchors {
      verticalCenter: label.verticalCenter

      left: label.left
    }
  }
}