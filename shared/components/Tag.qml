import QtQuick 2.15
import Qt.labs.platform 1.0

Rectangle {
  id: root
  
  property alias isShadowEnabled: titleLabel.isShadowEnabled
  property alias name: titleLabel.text
  property var address

  color: hoverHandler.hovered ? Qt.rgba(1, 1, 1, 0.375) : Qt.rgba(255, 255, 255, 0.25)
  opacity: mouseDownHandler.active ? 0.5 : 1
  radius: height / 2

  width: icon.x + icon.width + 3
  height: 20

  HoverHandler {
    id: hoverHandler
    
    cursorShape: Qt.PointingHandCursor
  }

  TapHandler {
    acceptedButtons: Qt.LeftButton

    onTapped: {
      if (root.address) {
        Qt.openUrlExternally(root.address)
      }
    }
  }

  PointHandler {
    id: mouseDownHandler

    acceptedButtons: Qt.LeftButton
  }

  PointHandler {
    acceptedButtons: Qt.RightButton
    enabled: address
    
    onActiveChanged: {
      if (active) {
        contextMenu.open()
      }
    }
  }

  // --- Title ---

  Label {
    id: titleLabel

    style: kTitleSecondary
    verticalAlignment: Qt.AlignVCenter

    x: 8
    height: parent.height
  }

  // --- Icon ---

  Image {
    id: icon

    source: '../resources/link.png'

    x: titleLabel.x + titleLabel.width + 5
    y: 3
    width: 14
    height: width
  }

  // --- Context Menu ---

  // Invisible text input to interface with system clipboard
  TextInput {
    id: textInput

    visible: false
  }

  Menu {
    id: contextMenu

    MenuItem {
      text: 'Copy'

      onTriggered: {
        textInput.text = titleLabel.text
        textInput.selectAll()
        textInput.copy()
      }
    }

    MenuSeparator { }

    MenuItem {
      text: 'Copy Link Location'

      onTriggered: {
        textInput.text = root.address
        textInput.selectAll()
        textInput.copy()
      }
    }
  }
}
