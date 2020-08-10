import QtQuick 2.14
import Qt.labs.platform 1.0

Label {
  id: root

  property bool isContextMenuPreviouslyOpened: false
  property string address
  
  signal onClicked

  // color: mouseArea.containsMouse ? '#00A0FF' : '#FFF'
  style: kTitleSecondary
  font.underline: address ? mouseArea.containsMouse : false

  MouseArea {
    id: mouseArea
    
    acceptedButtons: Qt.LeftButton | Qt.RightButton
    cursorShape: Qt.PointingHandCursor
    hoverEnabled: true
    visible: address
    
    onClicked: {
      // Work around Qt bug where clicking outside of a link after the context menu opens triggers a click event
      // TODO: File bug report with Qt
      if (isContextMenuPreviouslyOpened) {
        isContextMenuPreviouslyOpened = false
        return
      }

      if (mouse.button === Qt.LeftButton) {
        root.onClicked()
        Qt.openUrlExternally(root.address)
      }
    }

    onPressed: {
      if (mouse.button === Qt.RightButton) {
        contextMenu.open()
        isContextMenuPreviouslyOpened = true
      }
    }

    anchors.fill: parent
  }

  // TODO: Add Python class to interface with clipboard through Qt
  Menu {
    id: contextMenu

    MenuItem {
      text: 'Copy'
    }

    MenuSeparator { }

    MenuItem {
      text: 'Copy Link Location'
    }
  }
}
