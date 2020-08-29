import QtQuick 2.14
import QtQuick.Controls 2.14

import Kale 1.0

import 'History'
import '../shared/components'

Item {
  id: root

  // Store reference to view model counterpart that can be set from main.qml
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
    
    Button {
      text: 'Play next song'

      onClicked: viewModel.MOCK_playNextSong()
    }

    Button {
      text: 'Move song to 75%'

      onClicked: viewModel.MOCK_moveTo75Percent()
    }
  }

  // --- Current Scrobble ---

  CurrentScrobble {
    id: currentScrobble

    percentage: viewModel ? viewModel.currentScrobblePercentage : 0
    isSelected: canDisplayCurrentScrobble && viewModel.selectedScrobbleIndex === -1
    trackTitle: canDisplayCurrentScrobble && viewModel.currentScrobbleData.trackTitle
    artistName: canDisplayCurrentScrobble && viewModel.currentScrobbleData.artistName
    lastfmIsLoved: canDisplayCurrentScrobble && viewModel.currentScrobbleData.lastfmIsLoved
    visible: canDisplayCurrentScrobble

    imageSource: {
      if (canDisplayCurrentScrobble && viewModel.currentScrobbleData.hasLastfmData) {
        return viewModel.currentScrobbleData.albumImageUrl
      }
      
      return ''
    }

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

  HistoryListModel {
    id: listModel

    historyReference: viewModel
  }

  HistoryList {
    model: listModel
    selectedScrobbleIndex: viewModel ? viewModel.selectedScrobbleIndex : -2

    // index is an argument passed through when the signal is triggered
    onSelect: viewModel.selectedScrobbleIndex = index
    onToggleLastfmIsLoved: viewModel.toggleLastfmIsLoved(index)

    anchors {
      top: currentScrobble.visible ? currentScrobble.bottom : currentScrobble.top
      right: parent.right
      bottom: parent.bottom
      left: parent.left

      // When current scrobble is collapsed, remove margin so spacing isn't duplicated
      topMargin: currentScrobble.visible ? 15 : 0
    }
  }
}