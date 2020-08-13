import QtQuick 2.14
import Qt.labs.platform 1.0

Menu {
  id: root

  property TextEdit text

  MenuItem {
    text: 'Copy'

    onTriggered: {
      // Check if no text is selected
      if (root.text.selectionStart === root.text.selectionEnd) {
        // If no text is selected, everything must be temporarily selected in order to copy it
        root.text.selectAll()
        root.text.copy()
        root.text.deselect()
      } else {
        root.text.copy()
      }
    }
  }
}
