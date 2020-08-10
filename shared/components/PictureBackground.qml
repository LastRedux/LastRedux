import QtQuick 2.14
import QtGraphicalEffects 1.0

Item {
  id: root

  property alias source: image.source

  states: State {
    name: 'loaded'
    when: image.status === Image.Ready

    PropertyChanges {
      target: overlay
      color: '#000'
      opacity: 0.5
    }

    PropertyChanges {
      target: reflection
      opacity: 1
    }
  }

  transitions: Transition {
    id: transition
    
    from: ''
    to: 'loaded'
    
    readonly property int transitionDuration: 450
    readonly property int transitionEasing: Easing.OutQuint

    ColorAnimation {
      target: overlay
      duration: transition.transitionDuration
      easing.type: transition.transitionEasing
    }

    PropertyAnimation {
      target: overlay
      property: 'opacity'
      duration: transition.transitionDuration
      easing.type: transition.transitionEasing
    }

    PropertyAnimation {
      target: reflection
      property: 'opacity'
      duration: transition.transitionDuration
      easing.type: transition.transitionEasing
    }
  }

  // --- Reflection ---
  ShaderEffectSource {
    id: reflectionSource

    sourceItem: blurredImage
    
    visible: false

    height: image.height

    anchors {
      top: parent.bottom
      right: parent.right
      left: parent.left
    }

    // Replicate same color overlay as image
    Rectangle {
      color: '#000'
      opacity: 0.5

      anchors.fill: parent
    }
  }

  OpacityMask {
    id: reflection

    maskSource: mask
    opacity: 0
    source: reflectionSource

    // Transformation matrix for vertical flip
    transform: Matrix4x4 {
      matrix: Qt.matrix4x4( 1, 0, 0, 0, 0, -1, 0, reflection.height, 0, 0, 1, 0, 0, 0, 0, 1)
    }
    
    height: image.height

    anchors {
      top: parent.bottom
      right: parent.right
      left: parent.left
    }
  }

  Item {
    id: mask

    visible: false

    height: image.height

    anchors {
      bottom: reflectionSource.top
      right: parent.right
      left: parent.left
    }

    LinearGradient {
      height: 55

      // Anchor at bottom to compensate for flipped final image
      anchors {
        bottom: parent.bottom
        right: parent.right
        left: parent.left
      }

      gradient: Gradient {
        GradientStop { position: 1; color: Qt.rgba(1, 1, 1, 0.25)}
        GradientStop { position: 0; color: Qt.rgba(1, 1, 1, 0)}
      }
    }
  }

  // --- Shadow ---
  LinearGradient {
    height: 3

    anchors {
      top: parent.bottom
      right: parent.right
      left: parent.left
    }

    gradient: Gradient {
      GradientStop { position: 0; color: Qt.rgba(0, 0, 0, 0.075)}
      GradientStop { position: 1; color: Qt.rgba(0, 0, 0, 0)}
    }
  }

  LinearGradient {
    height: 8

    anchors {
      top: parent.bottom
      right: parent.right
      left: parent.left
    }

    gradient: Gradient {
      GradientStop { position: 0; color: Qt.rgba(0, 0, 0, 0.075)}
      GradientStop { position: 1; color: Qt.rgba(0, 0, 0, 0)}
    }
  }

  LinearGradient {
    height: 16

    anchors {
      top: parent.bottom
      right: parent.right
      left: parent.left
    }

    gradient: Gradient {
      GradientStop { position: 0; color: Qt.rgba(0, 0, 0, 0.1)}
      GradientStop { position: 1; color: Qt.rgba(0, 0, 0, 0)}
    }
  }

  // --- Image ---
  Image {
    id: image

    fillMode: Image.PreserveAspectCrop
    visible: false

    anchors.fill: parent
  }

  FastBlur {
    id: blurredImage

    radius: 128
    source: image

    anchors.fill: image
  }

  // --- Image Overlay ---
  Rectangle {
    id: overlay

    color: '#111'
    opacity: 1
    
    anchors.fill: parent
  }
}