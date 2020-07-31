import QtQuick 2.14
import QtQuick.Window 2.14

import Kale 1.0

import './shared/components'
import './views'

Window {
  id: application

  color: '#171717'
  flags: Qt.Window
  title: 'LastRedux'
  visible: true

  minimumWidth: 860
  minimumHeight: 540
  width: 900
  height: 589

  ApplicationViewModel {
    id: applicationViewModel
  }

  Sidebar {
    id: sidebar

    viewModel: applicationViewModel

    anchors {
      top: parent.top
      bottom: parent.bottom
      left: parent.left
    }
  }

  ScrobbleDetailsViewModel {
    id: scrobbleDetailsViewModel

    application: applicationViewModel
  }

  ScrobbleDetails {
    id: scrobbleDetails

    viewModel: scrobbleDetailsViewModel

    anchors {
      top: parent.top
      right: parent.right
      bottom: parent.bottom
      left: sidebar.right
    }
  }

  Timer {
    interval: 1000
    repeat: true
    running: true

    onTriggered: applicationViewModel.checkForNewTrack()
  }
}