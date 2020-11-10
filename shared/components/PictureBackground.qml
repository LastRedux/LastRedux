import QtQuick 2.14
import QtGraphicalEffects 1.12

import Kale 1.0

Item {
  id: root

  property bool isBlurEnabled: true

  // Passthrough so source can be set from outside of component
  property alias source: image.source

  states: State {
    name: 'loaded'
    when: image && image.hasImage

    // After image is loaded, fade out image overlay and fade in reflection
    PropertyChanges {
      target: overlay
      color: '#000' // Switch to black overlay color after image load instead of gray
      opacity: isBlurEnabled ? 0.5 : 0.75
    }

    PropertyChanges {
      target: reflection
      opacity: 1
    }
  }

  transitions: Transition {
    id: transition
    
    // Only run transition when switching to loaded from initial state
    // When the image is swapped out the component will instantly switch back to initial state
    from: ''
    to: 'loaded'
    
    readonly property int transitionDuration: 450
    readonly property int transitionEasing: Easing.OutQuint

    // Animate all properties with the same duration
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

  // Clone rendered texture of the already blurred image in order to add a color overlay to it
  ShaderEffectSource {
    id: reflectionSource

    sourceItem: blurredImage
    
    visible: false // This will then be masked, so render off screen at first

    height: image ? image.height : 0

    anchors {
      top: parent.bottom
      right: parent.right
      left: parent.left
    }

    // Replicate same color overlay as image
    Rectangle {
      color: '#000'
      opacity: isBlurEnabled ? 0.5 : 0.75

      anchors.fill: parent
    }
  }

  OpacityMask {
    id: reflection

    maskSource: mask
    opacity: 0 // Will be faded in through component state once image loads
    source: reflectionSource // Apply mask to the cloned, recolored image
    visible: isBlurEnabled

    // Use transformation matrix to vertically flip view
    // Must be done on final shown item, doesn't work if used on item earlier in chain like ShaderEffectSource
    transform: Matrix4x4 {
      matrix: Qt.matrix4x4( 1, 0, 0, 0, 0, -1, 0, reflection.height, 0, 0, 1, 0, 0, 0, 0, 1)
    }
    
    height: image ? image.height : 0

    anchors {
      top: parent.bottom
      right: parent.right
      left: parent.left
    }
  }

  // Mask must be as big as image so a container is used
  Item {
    id: mask

    visible: false

    height: image ? image.height : 0

    anchors {
      bottom: reflectionSource.top
      right: parent.right
      left: parent.left
    }

    Image {
      fillMode: Image.TileHorizontally
      source: '../resources/effects/trackDetailsReflectionMask.png'
      
      height: 55

      // Anchor at bottom to compensate for flipped final image
      anchors {
        bottom: parent.bottom
        right: parent.right
        left: parent.left
      }
    }
  }

  // --- Shadow and Border ---

  Image {
    fillMode: Image.TileHorizontally
    source: '../resources/effects/trackDetailsShadow.png'

    height: 16

    // Position outside of and under bounding box
    anchors {
      top: parent.bottom
      right: parent.right
      left: parent.left
    }
  }

  Rectangle {
    color: Qt.rgba(0, 0, 0, 0.23)

    height: 1

    anchors {
      top: parent.bottom
      right: parent.right
      left: parent.left
    }
  }

  // --- Image ---

  // Invisible image that will be blurred and then reflected
  NetworkImage {
    id: image

    shouldBlankOnNewSource: true
    visible: !isBlurEnabled

    anchors.fill: parent
  }

  // Blurred image stretched over the main area
  FastBlur {
    id: blurredImage

    cached: true // Redraw only when image is changed, not every frame
    radius: 128
    source: image
    visible: isBlurEnabled

    anchors.fill: image
  }

  // --- Image Overlay ---

  // Functions as placeholder background when no image is loaded, otherwise is used to darken the image
  Rectangle {
    id: overlay

    color: '#111'
    opacity: 1
    
    anchors.fill: parent
  }
}