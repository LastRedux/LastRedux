import QtQuick 2.14

import Kale 1.0

import 'History'
import '../shared/components'

Item {
  id: root

  // Store reference to view model and list model counterparts that can be set from main.qml
  property HistoryListModel listModel
  property HistoryViewModel viewModel

  property bool canDisplayCurrentScrobble: !!(viewModel && viewModel.currentScrobble)

  // --- Mock Player Plugin Controls ---

  Column {
    id: mockPlayerPluginControls

    spacing: 8
    visible: viewModel && viewModel.isUsingMockPlayer

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
    property bool hasLastfmData: {
      canDisplayCurrentScrobble ?
        !!viewModel.currentScrobble.lastfm_track :
        false
    }
    property bool hasAlbumArt: {
      canDisplayCurrentScrobble ?
          !!viewModel.currentScrobble.image_set :
          false
    }
    
    id: currentScrobbleView
    visible: canDisplayCurrentScrobble

    mediaPlayerName: viewModel ? viewModel.mediaPlayerName : ''
    scrobblePercentage: viewModel ? viewModel.scrobblePercentage : undefined
    trackTitle: canDisplayCurrentScrobble ? viewModel.currentScrobble.track_title : ''
    artistName: canDisplayCurrentScrobble ? viewModel.currentScrobble.artist_name : ''
    lastfmIsLoved: hasLastfmData ? viewModel.currentScrobble.lastfm_track.is_loved : false
    imageSource: hasAlbumArt ? viewModel.currentScrobble.image_set.small_url : ''
    isSelected: canDisplayCurrentScrobble && viewModel.selectedScrobbleIndex === -1
    canLove: hasLastfmData

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
      top: currentScrobbleView.visible ? currentScrobbleView.bottom : currentScrobbleView.top
      right: parent.right
      bottom: parent.bottom
      left: parent.left

      // When current scrobble is collapsed, remove margin so spacing isn't duplicated
      topMargin: currentScrobbleView.visible ? 15 : 0
    }
  }

  Shortcut {
    sequence: 'Ctrl+]'
    context: Qt.ApplicationShortcut
    onActivated: {
      if (viewModel.selectedScrobbleIndex == -2 && !viewModel.currentScrobble) {
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