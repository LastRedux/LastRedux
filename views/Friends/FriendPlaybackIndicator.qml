import QtQuick 2.14

import '../../shared/components'

PlaybackIndicator {
  id: root

  property bool isTrackLoved: false

  readonly property int heartMaxDistanceFromEdge: 3

  Repeater {
    model: 5

    delegate: Item {
      id: heart

      visible: root.isTrackLoved

      opacity: {
        const verticalCenter = root.height / 2
        const distanceFromCenter = Math.abs(verticalCenter - y)
        return 1 - (distanceFromCenter / (root.height - heartMaxDistanceFromEdge))
      }

      x: -5 + (5 * model.index)
      y: root.height + heartMaxDistanceFromEdge
      width: 8
      height: 0

      Image {
        source: '../../shared/resources/friendHeart.png'

        x: -4
        y: -8
      }

      SequentialAnimation {
        loops: Animation.Infinite
        running: root.isTrackLoved

        NumberAnimation {
          target: heart
          property: 'y'
          to: heartMaxDistanceFromEdge * -1
          duration: (((Math.abs(model.index - 2) / 4) + 1) * 450) + (model.index * 10)
        }
      }
    }
  }
}