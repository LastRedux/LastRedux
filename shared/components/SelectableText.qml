import QtQuick 2.14

TextEdit {
  id: root

  color: '#FFF'
  readOnly: true
  renderType: Text.NativeRendering
  selectByMouse: true
  selectionColor: Qt.rgba(255, 255, 255, 0.15)
  wrapMode: Text.Wrap

  // Match style of standard label
  font {
    letterSpacing: 0.25
    weight: Font.Medium
  }

  MouseArea {
    acceptedButtons: Qt.RightButton
    cursorShape: Qt.IBeamCursor // Show correct cursor when hovering over text

    onPressed: {
      contextMenu.open()
    }

    anchors.fill: parent
  }

  // Add context menu to copy the content
  TextContextMenu {
    id: contextMenu

    text: root
  }
}