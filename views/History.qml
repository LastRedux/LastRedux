import QtQuick 2.14

import Kale 1.0

import 'History'
import '../shared/components'

Item {
  id: root

  // Store reference to view model and list model counterparts that can be set from main.qml
  property HistoryListModel listModel
  property HistoryViewModel viewModel

  property bool canDisplayCurrentScrobble: {
    // Don't do just viewModel && viewModel.scrobbleData because we need to return a bool value instead of an undefined viewModel.scrobbleData
    if (viewModel && viewModel.currentScrobbleData) {
      return true
    }

    return false
  }

  // --- Mock Player Plugin Controls ---

  Column {
    id: mockPlayerPluginControls

    spacing: 8
    visible: viewModel && viewModel.isUsingMockPlayerPlugin

    anchors {
      top: parent.top
      right: parent.right
      left: parent.left

      topMargin: 10
      leftMargin: 15
    }

    Label {
      style: kTitleTertiary
      text: 'Mock Player Plugin'
    }

    Row {
      LabelButton {
        isCompact: true
        title: '⏮'

        onClicked: viewModel.mock_event('previous')
      }

      LabelButton {
        isCompact: true
        title: '⏯'

        onClicked: viewModel.mock_event('playPause')
      }
      
      LabelButton {
        isCompact: true
        title: '⏩'

        onClicked: viewModel.mock_event('scrubForward')
      }

      LabelButton {
        isCompact: true
        title: '⏭'

        onClicked: viewModel.mock_event('next')
      }
    }
  }

  // --- Current Scrobble ---

  CurrentScrobble {
    id: currentScrobble

    mediaPlayerName: viewModel ? viewModel.mediaPlayerName : ''
    percentage: viewModel ? viewModel.currentScrobblePercentage : 0
    isSelected: canDisplayCurrentScrobble && viewModel.selectedScrobbleIndex === -1
    trackTitle: canDisplayCurrentScrobble && viewModel.currentScrobbleData.trackTitle
    artistName: canDisplayCurrentScrobble && viewModel.currentScrobbleData.artistName
    lastfmIsLoved: canDisplayCurrentScrobble && viewModel.currentScrobbleData.lastfmIsLoved
    canLove: canDisplayCurrentScrobble && viewModel.currentScrobbleData.hasLastfmData
    visible: canDisplayCurrentScrobble

    imageSource: canDisplayCurrentScrobble && viewModel.currentScrobbleData.albumImageUrl || ''

    // -1 represents the currently selected item in the scrobble history
    onSelect: viewModel.selectedScrobbleIndex = -1
    onToggleLastfmIsLoved: viewModel.toggleLastfmIsLoved(-1)
    
    anchors {
      top: mockPlayerPluginControls.visible ? mockPlayerPluginControls.bottom : parent.top
      right: parent.right
      left: parent.left

      topMargin: mockPlayerPluginControls.visible ? 15 : 10
    }
  }

  // --- History List ---

  HistoryList {
    canReload: !viewModel.shouldShowLoadingIndicator
    model: listModel
    selectedScrobbleIndex: viewModel ? viewModel.selectedScrobbleIndex : -2
    visible: viewModel && viewModel.isEnabled

    // index is an argument passed through when the signal is triggered
    onSelect: viewModel.selectedScrobbleIndex = index
    onToggleLastfmIsLoved: viewModel.toggleLastfmIsLoved(index)
    onReloadHistory: viewModel.reloadHistory()

    anchors {
      top: currentScrobble.visible ? currentScrobble.bottom : currentScrobble.top
      right: parent.right
      bottom: parent.bottom
      left: parent.left

      // When current scrobble is collapsed, remove margin so spacing isn't duplicated
      topMargin: currentScrobble.visible ? 15 : 0
    }
  }

  Shortcut {
    sequence: 'Ctrl+]'
    context: Qt.ApplicationShortcut
    onActivated: {
      if (viewModel.selectedScrobbleIndex == -2 && !viewModel.currentScrobbleData) {
        // Select first history item if there is scrobble selected and no current scrobble
        viewModel.selectedScrobbleIndex = 0
      } else {
        viewModel.selectedScrobbleIndex++
      }
    }
  }

  Shortcut {
    sequence: 'Ctrl+['
    context: Qt.ApplicationShortcut
    onActivated: viewModel.selectedScrobbleIndex--
  }
}