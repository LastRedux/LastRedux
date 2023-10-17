import QtQuick 2.14
import Qt5Compat.GraphicalEffects

Item {
  id: root

  readonly property int kPrimary: 0
  readonly property int kSecondary: 1
  readonly property int kBack: 2

  property bool isCompact: false
  property bool isEnabled: true
  property int style: kSecondary

  signal clicked

  opacity: isEnabled ? 1 : 0.5

  width: height
  height: isCompact ? 24 : 30

  BorderImage {
    id: backgroundImage

    horizontalTileMode: BorderImage.Repeat

    border {
      top: 15
      right: 15
      bottom: 15
      left: style === kBack ? 23 : 15
    }

    source: {
      let path = '../resources/buttons/'

      switch (style) {
      case kPrimary:
        path += 'primary'
        break
      case kSecondary:
        path += 'secondary'
        break
      case kBack:
        path += 'back'
      }

      if (isCompact) {
        path += '-compact'
      }

      return path + '.png'
    }

    anchors {
      fill: parent

      margins: -8
    }
  }

  ColorOverlay {
    color: 'white'
    source: backgroundImage

    opacity: {
      if (isEnabled) {
        if (mouseArea.containsPress) {
          if (style === kPrimary) {
            return 0.25
          }

          return 0.125
        }
      }

      return 0
    }

    anchors.fill: backgroundImage
  }

  MouseArea {
    id: mouseArea

    hoverEnabled: true

    onClicked: if (isEnabled) { root.clicked() }

    anchors.fill: parent
  }
}