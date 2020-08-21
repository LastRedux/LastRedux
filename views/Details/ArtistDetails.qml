import QtQuick 2.14

import '../../shared/components'

Item {
  id: root

  property url imageUrl
  property string name
  property string lastfmUrl
  property string bio
  property bool isReadMoreLinkVisible

  // Use var instead of int to support undefined
  property var lastfmGlobalListeners
  property var lastfmGlobalPlays
  property var lastfmPlays

  height: column.y + column.height + 30

  Column {
    id: column

    spacing: 15

    anchors {
      top: artistImageView.top
      right: parent.right
      left: artistImageView.right

      topMargin: 10
      rightMargin: 30
      leftMargin: 20
    }

    // --- Name ---
    Link {
      style: kTitlePrimary
      text: name
      address: lastfmUrl
      wrapMode: Text.Wrap

      width: parent.width
    }

    // --- Statistics ---
    Flow {
      id: statistics
      
      spacing: 20
      visible: !!lastfmGlobalListeners

      width: parent.width
      
      Statistic {
        title: 'Listeners'
        value: lastfmGlobalListeners
      }

      Statistic {
        title: 'Plays'
        value: lastfmGlobalPlays
      }

      Statistic {
        title: lastfmPlays === '1' ? 'Play in Library' : 'Plays in Library'
        value: lastfmPlays
      }
    }

    // --- Bio ---
    Column {
      spacing: 5

      width: parent.width

      SelectableText {
        text: bio || 'No Bio Available'

        width: parent.width
      }

      Link {
        elide: Text.ElideRight
        text: 'Read more on Last.fm'
        address: lastfmUrl
        visible: isReadMoreLinkVisible // Only show if bio exists

        width: parent.width
      }
    }
  }

  // --- Artist Image ---

  Picture {
    id: artistImageView

    type: kArtist

    source: imageUrl

    width: 106
    height: width

    anchors {
      top: parent.top
      left: parent.left

      margins: 30
    }
  }
}