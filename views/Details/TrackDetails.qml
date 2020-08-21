import QtQuick 2.14
import Qt.labs.platform 1.0

import '../../shared/components'
import '../../util/helpers.js' as Helpers

PictureBackground {
  id: root

  property string title
  property string lastfmUrl
  
  // var to support undefined
  property var lastfmGlobalListeners 
  property var lastfmGlobalPlays 
  property var lastfmPlays
  property var lastfmTags

  property string artistName
  property string artistLastfmUrl

  property string albumName
  property string albumLastfmUrl
  property url albumImageUrl

  source: albumImageUrl

  height: Math.max(albumImageView.y + albumImageView.height, tags.y + tags.height) + 30

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
    text: title
    address: lastfmUrl

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
    address: artistLastfmUrl

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
    address: albumLastfmUrl

    // Position to the right of leading text
    anchors {
      top: albumNameLeadingText.top
      right: trackNameView.right
      left: albumNameLeadingText.right
      
      leftMargin: 3
    }
  }

  // --- Plays ---
  
  Flow {
    id: statistics
    
    spacing: 20
    visible: lastfmPlays !== undefined

    anchors {
      top: albumNameView.bottom
      right: trackNameView.right
      left: trackNameView.left

      topMargin: 10
    }
    
    Statistic {
      title: 'Listeners'
      value: lastfmGlobalListeners
    }

    Statistic {
      title: 'Plays'
      value: lastfmGlobalPlays
    }

    Statistic {
      title: lastfmPlays === 1 ? 'Play in Library' : 'Plays in Library'
      value: lastfmPlays
      shouldAbbreviate: false
    }
  }

  // --- Tags ---
  
  Flow {
    id: tags

    spacing: 8
    
    anchors {
      top: statistics.bottom
      right: trackNameView.right
      left: trackNameView.left

      topMargin: 15
    }
    
    Repeater {
      model: lastfmTags

      delegate: Tag {
        name: modelData.name
        address: modelData.url
      }
    }
  }
}