import QtQuick 2.14
import QtQuick.Controls 2.14

import Kale 1.0

import 'ScrobbleHistory'
import '../shared/components'

Item {
  id: root

  // Store reference to view model counterpart that can be set from main.qml
  property ScrobbleHistoryViewModel viewModel

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

    percentage: viewModel && viewModel.currentScrobblePercentage
    isSelected: canDisplayCurrentScrobble && viewModel.selectedScrobbleIndex === -1
    name: canDisplayCurrentScrobble && viewModel.currentScrobbleData.name
    artist: canDisplayCurrentScrobble && viewModel.currentScrobbleData.artist
    visible: canDisplayCurrentScrobble

    imageSource: {
      if (canDisplayCurrentScrobble && viewModel.currentScrobbleData.isAdditionalDataDownloaded) {
        return viewModel.currentScrobbleData.albumImageUrl
      }
      
      return ''
    }

    // Set the selected scrobble index in the view model to -1, which represents the currently selected item in the scrobble history
    onSelect: viewModel.selectedScrobbleIndex = -1
    
    anchors {
      top: mockPlayerPluginControls.visible ? mockPlayerPluginControls.bottom : parent.top
      right: parent.right
      left: parent.left

      topMargin: mockPlayerPluginControls.visible ? 15 : 10
    }
  }

  // --- Scrobble History List ---

  ScrobbleHistoryListModel {
    id: listModel

    scrobbleHistoryReference: viewModel
  }

  ScrobbleHistoryList {
    model: listModel
    selectedScrobbleIndex: viewModel && viewModel.selectedScrobbleIndex

    // index is an argument passed through when the signal is triggered
    onSelect: viewModel.selectedScrobbleIndex = index

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