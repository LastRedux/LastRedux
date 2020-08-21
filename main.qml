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

  // --- Details ---
  
  // View model
  DetailsViewModel {
    id: detailsViewModel

    historyReference: historyViewModel
  }

  // View
  Details {
    id: details

    viewModel: detailsViewModel

    anchors {
      top: parent.top
      right: parent.right
      bottom: parent.bottom
      left: sidebar.right
    }
  }

  // --- History ---
  
  // View model
  HistoryViewModel {
    id: historyViewModel
  }

  // View (will be loaded into sidebar)
  Component {
    id: historyPage

    History {
      id: history

      viewModel: historyViewModel
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

      initialItem: historyPage

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
