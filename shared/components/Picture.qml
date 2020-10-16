import QtQuick 2.14
import QtGraphicalEffects 1.12

Image {
  id: root

  readonly property int kTrack: 0
  readonly property int kArtist: 1

  property int type: kTrack

  width: 34
  height: width

  layer {
    enabled: root.width === root.height

    effect: DropShadow {
      color: Qt.rgba(0, 0, 0, 0.4)
      radius: 3
      verticalOffset: 1
    }
  }

  Image {
    id: placeholder

    opacity: 1
    source: root.width === root.height ? `../resources/${type === kArtist ? 'artistP' : 'p'}laceholder.png` : ''
    
    anchors.fill: parent

    Rectangle {
      color: '#757575'
      visible: root.width !== root.height

      anchors.fill: parent
    }

    states: State {
      name: 'loaded'
      when: root.status === Image.Ready

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