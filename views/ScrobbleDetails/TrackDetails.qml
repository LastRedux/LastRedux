import QtQuick 2.14
import Qt.labs.platform 1.0

import '../../shared/components'

PictureBackground {
  id: root

  property string trackName
  property string trackLastFmUrl
  property var trackPlays // var to support undefined

  property string artistName
  property string artistLastFmUrl

  property string albumName
  property string albumLastFmUrl
  property url albumImageUrl

  source: albumImageUrl

  height: albumImageView.height + 30 * 2

  // --- Album Image ---

  Picture {
    id: albumImageView

    source: albumImageUrl

    width: 160

    anchors {
      top: parent.top
      left: parent.left

      margins: 30
    }
  }

  // --- Track Name ---

  Link {
    id: trackNameView
    
    elide: Text.ElideRight
    style: kTitlePrimary
    text: trackName
    address: trackLastFmUrl

    anchors {
      top: albumImageView.top
      right: parent.right
      left: albumImageView.right

      topMargin: 10
      rightMargin: 30
      leftMargin: 20
    }
  }

  // --- Artist Name ---

  Link {
    id: artistNameView

    elide: Text.ElideRight
    text: artistName
    address: artistLastFmUrl

    anchors {
      top: trackNameView.bottom
      right: trackNameView.right
      left: trackNameView.left

      topMargin: 5
    }
  }

  // --- Album Name ---
  
  Label {
    id: albumNameLeadingText

    style: kBodyPrimary
    text: 'from'

    anchors {
      top: artistNameView.bottom
      left: trackNameView.left

      topMargin: 5
    }
  }

  Link {
    id: albumNameView

    elide: Text.ElideRight
    text: albumName
    address: albumLastFmUrl

    // Position to the right of leading text
    anchors {
      top: albumNameLeadingText.top
      right: trackNameView.right
      left: albumNameLeadingText.right
      
      leftMargin: 3
    }
  }

  // --- Plays ---

  Label {
    style: kTitleTertiary
    visible: !!trackPlays

    text: {
      if (trackPlays) {
        if (trackPlays === '1') { // track plays is string, not int
          return '1 play'
        } else {
          return `${trackPlays} plays`
        }
      }

      return ''
    }

    anchors {
      top: albumNameView.bottom
      right: trackNameView.right
      left: trackNameView.left

      topMargin: 10
    }

    PointHandler {
      id: pointHandler

      acceptedButtons: Qt.RightButton
      
      onActiveChanged: {
        if (active) {
          playsContextMenu.open()
        }
      }
    }

    // Invisible text input to interface with system clipboard
    TextInput {
      id: playsTextInput

      visible: false
    }

    Menu {
      id: playsContextMenu

      MenuItem {
        text: 'Copy'

        onTriggered: {
          playsTextInput.text = trackPlays
          playsTextInput.selectAll()
          playsTextInput.copy()
        }
      }
    }
  }
}