import QtQuick 2.14
import QtQuick.Controls 2.14
import QtQuick.Window 2.14

import Kale 1.0

import './shared/components'
import './views'

Window {
  id: application

  color: '#171717'
  title: 'LastRedux'
  visible: true

  minimumWidth: 866
  minimumHeight: 540
  width: 900
  height: 589

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

  // --- Scrobble History ---
  
  // View model
  ScrobbleHistoryViewModel {
    id: scrobbleHistoryViewModel
  }

  // View (will be loaded into sidebar)
  Component {
    id: scrobbleHistoryPage

    ScrobbleHistory {
      id: scrobbleHistory

      viewModel: scrobbleHistoryViewModel
    }
  }

  // --- Sidebar ---

  SidebarBackground {
    id: sidebar

    anchors {
      top: parent.top
      bottom: parent.bottom
      left: parent.left
    }

    StackView {
      id: stackView

      initialItem: scrobbleHistoryPage

      anchors {
        top: tabBar.bottom
        right: parent.right
        bottom: parent.bottom
        left: parent.left
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
  }
}