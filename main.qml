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

  // --- Scrobble History ---
  
  // View model
  ScrobbleHistoryViewModel {
    id: scrobbleHistoryViewModel
  }

  // View
  Sidebar {
    id: sidebar

    viewModel: scrobbleHistoryViewModel

    anchors {
      top: parent.top
      bottom: parent.bottom
      left: parent.left
    }
  }

  // --- Scrobble Details ---
  
  // View model
  ScrobbleDetailsViewModel {
    id: scrobbleDetailsViewModel

    scrobbleHistoryReference: scrobbleHistoryViewModel
  }

  // View
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
}