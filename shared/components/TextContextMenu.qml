import QtQuick 2.14
import Qt.labs.platform 1.0

Item {
  id: root

  property TextEdit text

  MouseArea {
    acceptedButtons: Qt.RightButton
    cursorShape: Qt.IBeamCursor

    onPressed: {
      contextMenu.open()
    }

    anchors.fill: parent
  }

  Menu {
    id: contextMenu

    MenuItem {
      text: 'Copy'

      onTriggered: {
        if (root.text.selectionStart === root.text.selectionEnd) {
          root.text.selectAll()
          root.text.copy()
          root.text.deselect()
        } else {
          root.text.copy()
        }
      }
    }
  }
}
