import QtQuick 2.15
import Qt.labs.platform 1.0

Label {
  id: root

  property string address
  
  signal onClicked

  // color: mouseArea.containsMouse ? '#00A0FF' : '#FFF'
  style: kTitleSecondary

  // Don't show underline for links that don't have an address loaded
  font.underline: address ? hoverHandler.hovered : false 

  // Limit area of pointer handlers to visible text
  Item {
    width: root.contentWidth
    height: root.contentHeight

    HoverHandler {
      id: hoverHandler
      
      cursorShape: address ? Qt.PointingHandCursor : Qt.ArrowCursor
    }

    TapHandler {
      acceptedButtons: Qt.LeftButton

      onTapped: {
        root.onClicked()

        if (root.address) {
          Qt.openUrlExternally(root.address)
        }
      }
    }

    PointHandler {
      id: pointHandler

      acceptedButtons: Qt.RightButton
      enabled: !!address
      
      onActiveChanged: {
        if (active) {
          contextMenu.open()
        }
      }
    }
  }

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
