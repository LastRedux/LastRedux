import QtQuick 2.15

TextEdit {
  id: root

  property bool isContextMenuEnabled: true

  color: '#FFF'
  readOnly: true
  renderType: Text.NativeRendering
  selectByMouse: true
  selectionColor: Qt.rgba(1, 1, 1, 0.15)
  wrapMode: Text.Wrap

  // Match style of standard label
  font {
    letterSpacing: 0.25
    weight: Font.Normal
  }

  HoverHandler {
    id: hoverHandler
    
    cursorShape: Qt.IBeamCursor // Show correct cursor when hovering over text
  }

  PointHandler {
    id: pointHandler

    acceptedButtons: Qt.RightButton
    
    onActiveChanged: {
      if (isContextMenuEnabled && active) {
        contextMenu.open()
      }
    }
  }

  // Add context menu to copy the content
  TextContextMenu {
    id: contextMenu

    text: root
  }
}