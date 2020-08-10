import QtQuick 2.14
import QtGraphicalEffects 1.0

Image {
  id: root

  width: 33
  height: width

  layer {
    enabled: true

    effect: DropShadow {
      color: Qt.rgba(0, 0, 0, 0.4)
      radius: 3
      verticalOffset: 1
    }
  }

  Image {
    id: placeholder

    opacity: 1
    source: '../resources/placeholder.png'
    
    anchors.fill: parent

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