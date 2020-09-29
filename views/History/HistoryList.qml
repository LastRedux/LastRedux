import QtQuick 2.15

import '../../shared/components'

Item {
  id: root

  readonly property int transitionDuration: 450
  readonly property int transitionEasing: Easing.OutQuint

  property alias model: list.model
  property int selectedScrobbleIndex

  signal select(int index)
  signal toggleLastfmIsLoved(int index)

  // --- Header ---

  Label {
    id: title

    style: kTitleTertiary
    text: 'History'

    x: 15
  }

  // --- List ---

  ListView {
    id: list

    bottomMargin: 10 // Bottom padding must be added in list instead of anchors because content overflows into the margin zone when scrolling instead of being cut off
    clip: true // Prevent content from appearing outside the list's bounding box
    reuseItems: true

    // Transition for new items sliding in
    add: Transition {
      ParallelAnimation {
        // Slide in from offscreen
        NumberAnimation {
          duration: transitionDuration
          property: 'x'
          from: list.width * -1 // Set starting position
          easing.type: transitionEasing
        }

        // Fade in
        NumberAnimation {
          duration: transitionDuration
          property: 'opacity'
          to: 1
          easing.type: transitionEasing
        }
      }
    }

    // Transition for current items shifting down after insert
    addDisplaced: Transition {
      // Animate y to new position
      NumberAnimation {
        duration: transitionDuration
        property: 'y'
        easing.type: transitionEasing
      }
    }

    // Position under title
    anchors {
      top: title.bottom
      right: parent.right
      bottom: parent.bottom
      left: parent.left

      topMargin: 8
    }

    // --- Scrobble Item ---
    delegate: Scrobble {
      isSelected: {
        // -2 represents no selection because Qt doesn't understand Python's None value
        if (selectedScrobbleIndex !== -2) {
          return selectedScrobbleIndex === model.index
        }
        
        return false
      }

      trackTitle: model.trackTitle
      artistName: model.artistName
      timestamp: model.timestamp
      imageSource: model.hasLastfmData ? model.albumImageUrl : ''
      lastfmIsLoved: model.hasLastfmData ? model.lastfmIsLoved : false
      canLove: model.hasLastfmData

      onSelect: root.select(model.index)
      onToggleLastfmIsLoved: root.toggleLastfmIsLoved(model.index)

      width: list.width
    }
  }

  // Add native scrolling physics to scroll area
  WheelScrollArea {
    flickable: list

    anchors.fill: list
  }

  // Fade in shadow when list is scrolled down to prevent abrupt clipping
  ScrollAreaEdgeShadow {
    opacity: list.contentY - list.originY > 0

    anchors {
      top: list.top
      right: parent.right
      left: parent.left
    }
  }
}
