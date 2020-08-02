import QtQuick 2.14
import QtQuick.Controls 2.14

import Kale 1.0

import '../../views'

Rectangle {
  id: root

  property ScrobbleHistoryViewModel viewModel

  color: '#1E1E1E'

  width: 244

  StackView {
    id: stackView

    initialItem: scrobblesPage
    
    anchors {
      top: tabBar.bottom
      right: parent.right
      bottom: parent.bottom
      left: parent.left
    }
  }

  Component {
    id: scrobblesPage

    ScrobbleHistory {
      id: scrobbles

      viewModel: root.viewModel
    }
  }

  TabBarBackground {
    id: tabBar

    anchors {
      top: parent.top
      right: parent.right
      left: parent.left
    }
  }

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
