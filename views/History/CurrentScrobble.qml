import QtQuick 2.14

import '../../shared/components'

Column {
  id: root

  spacing: 8

  property string mediaPlayerName
  property var scrobblePercentage

  // Passthrough properties to scrobble view
  property alias isSelected: scrobbleView.isSelected
  property alias lastfmIsLoved: scrobbleView.lastfmIsLoved
  property alias canLove: scrobbleView.canLove
  property alias trackTitle: scrobbleView.trackTitle
  property alias artistName: scrobbleView.artistName
  property alias imageSource: scrobbleView.imageSource

  signal select
  signal toggleLastfmIsLoved

  // --- Header ---

  Item {
    width: parent.width

    // Match header height to the title's height
    height: title.height

    Label {
      id: title

      style: kTitleTertiary
      text: `LISTENING ON ${mediaPlayerName}`

      // Add left margin because layout of rest of column is edge-to-edge
      x: 15
    }

    ScrobbleMeter {
      id: scrobbleMeter

      percentage: scrobblePercentage
      visible: scrobblePercentage >= 0 // Don't show while loading track crop/length

      anchors {
        right: parent.right

        rightMargin: 15

        verticalCenter: parent.verticalCenter
      }
    }
  }

  // --- Scrobble ---

  Scrobble {
    id: scrobbleView

    // TODO: Add loved attribute
    
    onSelect: root.select()
    onToggleLastfmIsLoved: root.toggleLastfmIsLoved()
    
    width: parent.width
  }
}
