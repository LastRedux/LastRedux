import QtQuick 2.15
import Qt.labs.platform 1.0

Item {
  id: root
  
  property string address
  property string text

  property bool containsPress: hoverHandler.hovered && leftPointHandler.active
  property alias hovered: hoverHandler.hovered

  signal clicked

  // Invisible text input to interface with system clipboard
  TextInput {
    id: textInput

    visible: false
  }

  // --- Hover Handler ---
  
  HoverHandler {
    id: hoverHandler
    
    cursorShape: address ? Qt.PointingHandCursor : Qt.ArrowCursor
  }

  // --- Tap Handler ---
  
  TapHandler {
    acceptedButtons: Qt.LeftButton

    onTapped: {
      root.clicked()

      if (root.address) {
        Qt.openUrlExternally(root.address)
      }
    }
  }

  // --- Left Point Handler ---

  PointHandler {
    id: leftPointHandler

    acceptedButtons: Qt.LeftButton
    enabled: !!address
  }
  
  // --- Right Point Handler ---
  
  PointHandler {
    acceptedButtons: Qt.RightButton
    enabled: !!address
    
    onActiveChanged: {
      if (active) {
        contextMenu.open()
      }
    }
  }

  // --- Context Menu ---

  Menu {
    id: contextMenu

    MenuItem {
      text: 'Copy'

      onTriggered: {
        textInput.text = root.text
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