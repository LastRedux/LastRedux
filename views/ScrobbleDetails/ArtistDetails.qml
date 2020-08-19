import QtQuick 2.14

import '../../shared/components'

Item {
  id: root

  property url imageUrl
  property string name
  property string lastFmUrl
  property string bio
  property bool isReadMoreLinkVisible

  // Strings because view model should provide formatted numbers with commas
  property string globalListeners
  property string globalPlays
  property string plays

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
      address: lastFmUrl
      wrapMode: Text.Wrap

      width: parent.width
    }

    // --- Statistics ---
    Flow {
      id: statistics
      
      spacing: 20
      visible: globalListeners

      width: parent.width
      
      Statistic {
        title: 'Listeners'
        value: globalListeners
      }

      Statistic {
        title: 'Plays'
        value: globalPlays
      }

      Statistic {
        title: plays === '1' ? 'Play in Library' : 'Plays in Library'
        value: plays
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
        address: lastFmUrl
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