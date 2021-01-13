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
  property bool hasAttemptedLogin: false
  property bool shouldShowProfileLoadingIndicator: true
  property bool shouldShowFriendsLoadingIndicator: true

  // property bool isInMiniMode: {
  //   if (detailsViewModel) {
  //     if (detailsViewModel.isInMiniMode) {
  //       return true
  //     }
  //   }

  //   return false
  // }

  color: '#171717'
  flags: Qt.CustomizeWindowHint | Qt.WindowTitleHint | Qt.WindowCloseButtonHint | Qt.WindowMinMaxButtonsHint // Disable fullscreen on macOS
  title: 'LastRedux'
  visible: true

  // minimumWidth: isInMiniMode ? 0 : 755
  // minimumHeight: isInMiniMode ? 0 : 470
  width: 957
  height: 600

  function switchToTab(tabIndex, isSameTab) {
    if (historyViewModel.isEnabled) {
      if (currentTabIndex !== tabIndex || isSameTab) {
        currentTabIndex = tabIndex

        switch (tabIndex) {
        case 1:
          profileViewModel.loadProfile(shouldShowProfileLoadingIndicator)
          shouldShowProfileLoadingIndicator = false
          break
        case 2:
          friendsViewModel.loadFriends(shouldShowFriendsLoadingIndicator)
          shouldShowFriendsLoadingIndicator = false
        }
      }
    }
  }

  onActiveChanged: {
    if (active) {
      // Wait until first window focus to attempt login
      if (!hasAttemptedLogin) {
        hasAttemptedLogin = true
        attemptLoginTimer.running = true
      }

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

  // Wait 100ms after the window loads because onboarding window dissapears if shown immediately
  Timer {
    id: attemptLoginTimer
    
    interval: 100

    onTriggered: applicationViewModel.attemptLogin()
  }

  FontLoaders {
    id: fontLoaders
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

      MenuSeparator { }

      // MenuItem {
      //   text: qsTr('Toggle Mini Mode')

      //   onTriggered: historyViewModel.toggleMiniMode()
      // }

      MenuItem {
        text: qsTr('Use Music App as Media Player')

        onTriggered: historyViewModel.switchToMediaPlugin('musicApp')
      }

      MenuItem {
        text: qsTr('Use Spotify as Media Player')

        onTriggered: historyViewModel.switchToMediaPlugin('spotify')
      }

      MenuSeparator { }
      
      MenuItem {
        text: qsTr('LastRedux Private Beta 1')
        enabled: false
      }

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

  ApplicationViewModel {
    id: applicationViewModel

    onOpenOnboarding: onboardingWindow.show()
    onCloseOnboarding: onboardingWindow.hide()
  }

  // --- Onboarding ---
  
  OnboardingViewModel {
    id: onboardingViewModel

    applicationReference: applicationViewModel

    onOpenUrl: address => {
      Qt.openUrlExternally(address)
    }
  }
  
  Window {
    id: onboardingWindow

    color: '#1f1f1f'
    modality: Qt.WindowModal
    // visible: true

    minimumWidth: 632
    minimumHeight: 427
    maximumWidth: 632
    maximumHeight: 427
    
    Onboarding {
      viewModel: onboardingViewModel

      anchors.fill: parent
    }
  }

  // --- Details ---
  
  // DetailsViewModel {
  //   id: detailsViewModel

  //   historyReference: historyViewModel
  // }

  // Details {
  //   id: details

  //   viewModel: detailsViewModel
  //   onSwitchToCurrentScrobble: historyViewModel.selectedScrobbleIndex = -1

  //   anchors {
  //     top: parent.top
  //     right: parent.right
  //     bottom: parent.bottom
  //     left: isInMiniMode ? parent.left : sidebar.right
  //   }
  // }

  // // --- History Page ---

  HistoryViewModel {
    id: historyViewModel

    applicationReference: applicationViewModel
    onShowNotification: (title, message) => trayIcon.showMessage(title, message)
  }

  HistoryListModel {
    id: historyListModel

    historyReference: historyViewModel
  }

  // --- Profile Page ---

  ProfileViewModel {
    id: profileViewModel

    applicationReference: applicationViewModel
  }

  // --- Friends Page ---

  FriendsViewModel {
    id: friendsViewModel

    applicationReference: applicationViewModel
  }

  FriendsListModel {
    id: friendsListModel

    friendsReference: friendsViewModel
  }

  // // --- Sidebar ---

  SidebarBackground {
    id: sidebar

    visible: true //isInMiniMode ? false : true

    anchors {
      top: parent.top
      bottom: parent.bottom
      left: parent.left
    }

    Item {
      clip: true

      anchors {
        top: tabBar.bottom
        right: parent.right
        bottom: parent.bottom
        left: parent.left
      }

      History {
        id: history

        listModel: historyListModel
        viewModel: historyViewModel
        visible: currentTabIndex === 0

        anchors.fill: parent
      }

      Profile {
        id: profile

        viewModel: profileViewModel
        visible: currentTabIndex === 1

        anchors.fill: parent
      }

      Friends {
        id: friends

        listModel: friendsListModel
        viewModel: friendsViewModel
        visible: currentTabIndex === 2

        anchors.fill: parent
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
        visible: true //historyViewModel.isEnabled

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
