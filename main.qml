import QtQuick 2.14
import QtQuick.Controls 2.14
import QtQuick.Window 2.14

import Kale 1.0

import './shared/components'
import './views'

Window {
  id: application

  property bool isOnProfilePage: false

  color: '#171717'
  title: 'LastRedux'
  visible: true

  minimumWidth: 755 //866
  minimumHeight: 470 //540
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

  // --- History Page ---
  
  // View model
  HistoryListModel {
    id: historyListModel

    historyReference: historyViewModel
  }

  HistoryViewModel {
    id: historyViewModel
  }

  // View (will be loaded into sidebar)
  Component {
    id: historyPage

    History {
      id: history

      listModel: historyListModel
      viewModel: historyViewModel
    }
  }

  // --- Profile Page ---

  Component {
    id: profilePage

    Profile {
      id: profile
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

      clip: true
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

      Button {
        text: 'Switch Tab'

        onClicked: {
          if (isOnProfilePage) {
            stackView.replace(historyPage)
            isOnProfilePage = false
            return
          }

          stackView.replace(profilePage)
          isOnProfilePage = true
        }
        
        anchors.centerIn: parent
      }
    }
  }
}
