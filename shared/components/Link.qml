import QtQuick 2.14
import Qt.labs.platform 1.0

Label {
  id: root
  
  signal onClicked

  // color: mouseArea.containsMouse ? '#00A0FF' : '#FFF'
  style: kTitleSecondary
  font.underline: mouseArea.containsMouse

  MouseArea {
    id: mouseArea
    
    acceptedButtons: Qt.LeftButton | Qt.RightButton
    cursorShape: Qt.PointingHandCursor
    hoverEnabled: true
    
    onClicked: {
      if (mouse.button === Qt.LeftButton) {
        root.onClicked()
      }
    }

    onPressed: {
      if (mouse.button === Qt.RightButton) {
        contextMenu.open()
      }
    }

    anchors.fill: parent
  }

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
