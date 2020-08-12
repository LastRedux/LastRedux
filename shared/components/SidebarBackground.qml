import QtQuick 2.14

Rectangle {
  id: root

  color: '#1E1E1E'

  width: 250

  // Border
  Rectangle {
    color: Qt.rgba(0, 0, 0, 0.25)

    width: 1

    anchors {
      top: parent.top
      bottom: parent.bottom
      left: parent.right
    }
  }
}
