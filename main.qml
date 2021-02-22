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
  property bool isInMiniMode: (applicationViewModel && applicationViewModel.isInMiniMode) || false
  property int cachedWindowWidth: 957
  property int cachedWindowHeight: 600

  color: '#171717'
  flags: Qt.CustomizeWindowHint | Qt.WindowTitleHint | Qt.WindowCloseButtonHint | Qt.WindowMinMaxButtonsHint // Disable fullscreen on macOS
  title: 'LastRedux'
  visible: true

  minimumWidth: isInMiniMode ? 0 : 755
  minimumHeight: isInMiniMode ? 0 : 470

  width: cachedWindowWidth
  height: cachedWindowHeight

  function switchToTab(tabIndex, isSameTab) {
    if (historyViewModel.isEnabled) {
      if (currentTabIndex !== tabIndex || isSameTab) {
        currentTabIndex = tabIndex

        switch (tabIndex) {
        case 1:
          profileViewModel.loadProfile()
          break
        case 2:
          friendsViewModel.loadFriends()
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
      
      // Automatically refresh currently selected tab as if it was just switched to
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

      MenuSeparator {
        visible: historyViewModel.isSpotifyPluginAvailable
      }

      MenuItem {
        text: isInMiniMode ? qsTr('Switch from Mini Mode') : qsTr('Switch to Mini Mode')

        onTriggered: {
          // Update isInMiniMode value in details view model
          applicationViewModel.toggleMiniMode()
        }
      }

      MenuItem {
        checkable: true
        checked: historyViewModel.isDiscordRichPresenceEnabled
        text: qsTr('Enable Discord Rich Presence')

        onTriggered: historyViewModel.isDiscordRichPresenceEnabled = checked
      }

      MenuItem {
        text: qsTr('Use Music App as Media Player')
        visible: historyViewModel.isSpotifyPluginAvailable && detailsViewModel.mediaPlayerName != 'Music'

        onTriggered: historyViewModel.switchToMediaPlugin('musicApp')
      }

      MenuItem {
        text: qsTr('Use Spotify as Media Player')
        visible: historyViewModel.isSpotifyPluginAvailable && detailsViewModel.mediaPlayerName != 'Spotify'

        onTriggered: historyViewModel.switchToMediaPlugin('spotify')
      }

      MenuSeparator { }
      
      MenuItem {
        text: qsTr('LastRedux Private Beta 2')
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

    onOpenOnboarding: {
      onboardingWindow.show()
    }
    
    onCloseOnboarding: onboardingWindow.hide()
    onShowNotification: (title, message) => trayIcon.showMessage(title, message)

    onIsInMiniModeChanged: {
      if (isInMiniMode) {
        // Save dimensions to restore later
        cachedWindowWidth = application.width
        cachedWindowHeight = application.height

        application.width = 615
        application.height = 400
      } else {
        // Restore old dimensions
        application.width = cachedWindowWidth
        application.height = cachedWindowHeight
      }
    }
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
  
  DetailsViewModel {
    id: detailsViewModel

    historyReference: historyViewModel
    applicationReference: applicationViewModel
  }

  Details {
    id: details

    isInMiniMode: application.isInMiniMode
    viewModel: detailsViewModel
    onSwitchToCurrentScrobble: historyViewModel.selectedScrobbleIndex = -1

    // Hide media player name while it's still being retrieved from the database
    shouldShowMediaPlayerName: historyViewModel.isEnabled

    anchors {
      top: parent.top
      right: parent.right
      bottom: parent.bottom
      left: application.isInMiniMode ? parent.left : sidebar.right
    }
  }

  // --- History Page ---

  HistoryViewModel {
    id: historyViewModel

    applicationReference: applicationViewModel
    onPreloadProfileAndFriends: {
      profileViewModel.loadProfile()
      friendsViewModel.loadFriends()
    }
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

    visible: isInMiniMode ? false : true

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
        visible: true

        anchors {
          fill: parent

          topMargin: 22
        }

        Row {
          spacing: 29

          anchors.centerIn: parent

          TabBarItem {
            iconName: 'history'
            isLoading: historyViewModel && historyViewModel.isLoading
            isSelected: currentTabIndex === 0

            onClicked: switchToTab(0)
          }

          TabBarItem {
            iconName: 'profile'
            isLoading: profileViewModel && profileViewModel.isLoading
            isSelected: currentTabIndex === 1

            onClicked: switchToTab(1)
          }

          TabBarItem {
            iconName: 'friends'
            isLoading: friendsViewModel && friendsViewModel.isLoading
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

  Shortcut {
    sequence: 'Ctrl+Shift+m'
    context: Qt.ApplicationShortcut
    onActivated: applicationViewModel.toggleMiniMode()
  }
}
