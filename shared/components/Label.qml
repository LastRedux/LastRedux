import QtQuick 2.14
import Qt5Compat.GraphicalEffects

Text {
  readonly property int kLargeTitle: 0
  readonly property int kTitlePrimary: 1
  readonly property int kTitleSecondary: 2
  readonly property int kTitleTertiary: 3
  readonly property int kCaption: 4
  readonly property int kBodyPrimary: 5
  readonly property int kBodySecondary: 6
  readonly property int kNumber: 7
  readonly property int kBodyPrimarySystem: 9

  property bool isShadowEnabled: true
  property int style: kBodyPrimary
  
  color: '#FFF'
  linkColor: color
  opacity: style === kTitleTertiary ? 0.81 : 1
  renderType: Text.NativeRendering

  font {
    capitalization: style === kTitleTertiary ? Font.AllUppercase : Font.MixedCase
    family: fontLoaders.name
    
    letterSpacing: {
      switch (style) {
      case kLargeTitle:
        return -0.75
      case kTitlePrimary:
      case kNumber:
        return -0.1
      case kTitleTertiary:
        return 0.1
      case kTitleSecondary:
      case kCaption:
        return 0
      default:
        return 0.2
      }
    }

    pixelSize: {
      switch (style) {
      case kLargeTitle:
        return 29
      case kTitlePrimary:
        return 26
      case kTitleTertiary:
        return 11
      case kBodySecondary:
        return 12
      case kNumber:
        return 20
      default:
        return 13
      }
    }

    weight: {
      switch (style) {
      case kCaption:
        return Font.DemiBold
      case kBodyPrimary:
        return Font.Medium
      case kBodyPrimarySystem:
        return Font.Normal
      default:
        return Font.Bold
      }
    }
  }

  layer {
    enabled: isShadowEnabled

    effect: DropShadow {
      color: '#131313'
      radius: 0
      verticalOffset: -1
    }
  }
}
