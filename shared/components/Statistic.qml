import QtQuick 2.14
import Qt.labs.platform 1.0

import '../../util/helpers.js' as Helpers

Item {
  property bool shouldAbbreviate: true
  property string title
  property var value
  
  width: column.width
  height: column.height

  Column {
    id: column
    
    spacing: 3

    Label {
      style: kNumber
      
      text: {
        if (value === undefined) {
          return ''
        }

        if (shouldAbbreviate) {
          return Helpers.abbreviateNumber(value)
        }

        return Helpers.numberWithCommas(value)
      }
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
