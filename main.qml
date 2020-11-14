import QtQuick 2.14
import QtQuick.Controls 2.14 as Controls
import QtQuick.Window 2.14
import Qt.labs.platform 1.1

import Kale 1.0

import './shared/components'
import './views'

Window {
  id: application

  property int currentTabIndex: 0
  property bool shouldShowProfileLoadingIndicator: true
  property bool shouldShowFriendsLoadingIndicator: true

  property bool isInMiniMode: {
    if (historyViewModel) {
      if (historyViewModel.miniMode) {
        return true
      }
    }

    return false
  }

  property alias isInMiniMode: details.isInMiniMode

  color: '#171717'
  title: 'LastRedux'
  visible: true

  minimumWidth: isInMiniMode ? 0 : 755
  minimumHeight: isInMiniMode ? 0 : 470
  width: 957
  height: 600

  function switchToTab(tabIndex, isSameTab) {
    if (currentTabIndex !== tabIndex || isSameTab) {
      currentTabIndex = tabIndex

      switch (tabIndex) {
      case 0:
        if (!isSameTab) {
          stackView.replace(historyPage)
        }
        
        break
      case 1:
        if (!isSameTab) {
          stackView.replace(profilePage)
        }

        profileViewModel.loadProfileAndTopArtists(shouldShowProfileLoadingIndicator)
        shouldShowProfileLoadingIndicator = false
        break
      case 2:
        if (!isSameTab) {
          stackView.replace(friendsPage)
        }
        
        friendsViewModel.loadFriends(shouldShowFriendsLoadingIndicator)
        shouldShowFriendsLoadingIndicator = false
      }
    }
  }

  onActiveChanged: {
    if (active) {
      shouldShowProfileLoadingIndicator = true
      shouldShowFriendsLoadingIndicator = true
      switchToTab(currentTabIndex, true)
    }
  }

  onClosing: { 
    application.hide()

    // Prevent the window close event from being accepted by the system
    close.accepted = false // close is a hidden parameter to the onClosing function
  }

  FontLoaders {
    id: fontLoaders
  }

  Window {
    id: onboardingWindow

    color: '#1f1f1f'
    modality: Qt.WindowModal

    minimumWidth: 632
    minimumHeight: 427
    maximumWidth: 632
    maximumHeight: 427
    
    Onboarding {
      anchors.fill: parent
    }
  }

  SystemTrayIcon {
    id: trayIcon

    visible: true
    icon.source: 'shared/resources/trayIcon.png'
    icon.mask: true

    menu: Menu {
      MenuItem {
        text: qsTr('Show Window')
        shortcut: 'Ctrl+Meta+S'

        onTriggered: {
          application.show()
          application.raise()
          application.requestActivate()
        }
      }

      MenuItem {
        text: qsTr('Open Onboarding...')

        onTriggered: onboardingWindow.show()
      }

      MenuItem {
        text: qsTr('Toggle mini mode')

        onTriggered: historyViewModel.toggleMiniMode()
      }
      
      MenuItem {
        text: qsTr('Preferences...')
        shortcut: StandardKey.Preferences

        onTriggered: trayIcon.showMessage('', 'If you are seeing this, welcome to the early commit zone :)')
      }

      MenuSeparator { }

      MenuItem {
        text: qsTr('Quit LastRedux')
        shortcut: StandardKey.Quit

        onTriggered: {
          // Close the application window to deallocate its resources before quitting (otherwise PySide crashes)
          application.close()

          Qt.quit()
        }
      }
    }
  }

  // --- Details ---
  
  DetailsViewModel {
    id: detailsViewModel

    historyReference: historyViewModel
  }

  Details {
    id: details

    viewModel: detailsViewModel
    onSwitchToCurrentScrobble: historyViewModel.selectedScrobbleIndex = -1

    anchors {
      top: parent.top
      right: parent.right
      bottom: parent.bottom
      left: isInMiniMode ? parent.left : sidebar.right
    }
  }

  // --- History Page ---

  HistoryViewModel {
    id: historyViewModel

    onShowNotification: (title, message) => trayIcon.showMessage(title, message)
  }

  HistoryListModel {
    id: historyListModel

    historyReference: historyViewModel
  }

  Component {
    id: historyPage

    History {
      id: history

      listModel: historyListModel
      viewModel: historyViewModel
    }
  }

  // --- Profile Page ---

  ProfileViewModel {
    id: profileViewModel
  }

  Component {
    id: profilePage

    Profile {
      id: profile

      viewModel: profileViewModel
    }
  }

  // --- Friends Page ---

  FriendsViewModel {
    id: friendsViewModel
  }

  FriendsListModel {
    id: friendsListModel

    friendsReference: friendsViewModel
  }

  Component {
    id: friendsPage

    Friends {
      id: friends

      listModel: friendsListModel
      viewModel: friendsViewModel
    }
  }

  // --- Sidebar ---

  SidebarBackground {
    id: sidebar

    visible: isInMiniMode ? false : true

    anchors {
      top: parent.top
      bottom: parent.bottom
      left: parent.left
    }

    Controls.StackView {
      id: stackView

      clip: true
      initialItem: historyPage
      replaceEnter: Transition { }
      replaceExit: Transition { }

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

      Item {
        clip: true

        anchors {
          fill: parent

          topMargin: 22
        }

        Row {
          spacing: 29

          anchors.centerIn: parent

          TabBarItem {
            iconName: 'history'
            shouldShowLoadingIndicator: historyViewModel && historyViewModel.shouldShowLoadingIndicator
            isSelected: currentTabIndex === 0

            onClicked: switchToTab(0)
          }

          TabBarItem {
            iconName: 'profile'
            shouldShowLoadingIndicator: profileViewModel && profileViewModel.shouldShowLoadingIndicator
            isSelected: currentTabIndex === 1

            onClicked: switchToTab(1)
          }

          TabBarItem {
            iconName: 'friends'
            shouldShowLoadingIndicator: friendsViewModel && friendsViewModel.shouldShowLoadingIndicator
            isSelected: currentTabIndex === 2

            onClicked: switchToTab(2)
          }
        }
      }
    }
  }

  Shortcut {
    sequence: 'Ctrl+1'
    context: Qt.ApplicationShortcut
    onActivated: switchToTab(0)
  }

  Shortcut {
    sequence: 'Ctrl+2'
    context: Qt.ApplicationShortcut
    onActivated: switchToTab(1)
  }

  Shortcut {
    sequence: 'Ctrl+3'
    context: Qt.ApplicationShortcut
    onActivated: switchToTab(2)
  }
}
