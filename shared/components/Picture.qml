import QtQuick 2.14
import QtGraphicalEffects 1.12

import Kale 1.0

Item {
  id: root

  readonly property int kTrack: 0
  readonly property int kArtist: 1

  property int type: kTrack
  property alias source: networkImage.source
  property alias shouldBlankOnNewSource: networkImage.shouldBlankOnNewSource

  width: 34
  height: 34

  layer {
    enabled: root.width === root.height

    effect: DropShadow {
      color: Qt.rgba(0, 0, 0, 0.4)
      radius: 3
      verticalOffset: 1
    }
  }

  NetworkImage {
    id: networkImage

    shouldBlankOnNewSource: true

    anchors.fill: parent
  }

  Image {
    id: placeholder

    source: root.width === root.height ? `../resources/${type === kArtist ? 'artistP' : 'p'}laceholder.png` : ''
    
    anchors.fill: parent

    Rectangle {
      color: '#757575'
      visible: root.width !== root.height

      anchors.fill: parent
    }

    states: State {
      name: 'loaded'
      when: networkImage && networkImage.hasImage

      PropertyChanges {
        target: placeholder
        opacity: 0
      }
    }

    transitions: Transition {
      from: ''
      to: 'loaded'

      PropertyAnimation {
        target: placeholder
        property: 'opacity'
        duration: 450
        easing.type: Easing.OutQuint
      }
    }
  }
}