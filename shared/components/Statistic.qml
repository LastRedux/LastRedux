import QtQuick 2.14
import Qt.labs.platform 1.0

Item {
  property string title
  property string value
  
  width: column.width
  height: column.height

  Column {
    id: column
    
    spacing: 3

    Label {
      style: kNumber
      text: value
    }

    Label {
      style: kTitleTertiary
      text: title
    }
  }

  // Show context menu on right click
  PointHandler {
    id: pointHandler

    acceptedButtons: Qt.RightButton
    
    onActiveChanged: {
      if (active) {
        contextMenu.open()
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
        textInput.text = value
        textInput.selectAll()
        textInput.copy()
      }
    }
  }
}