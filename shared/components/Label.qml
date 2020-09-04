import QtQuick 2.14
import QtGraphicalEffects 1.0

Text {
  readonly property int kTitlePrimary: 0
  readonly property int kTitleSecondary: 1
  readonly property int kTitleTertiary: 2
  readonly property int kCaption: 3
  readonly property int kBodyPrimary: 4
  readonly property int kBodySecondary: 5
  readonly property int kNumber: 6

  property bool isShadowEnabled: true
  property int style: kBodyPrimary
  
  color: '#FFF'
  opacity: style === kTitleTertiary ? 0.81 : 1
  renderType: Text.NativeRendering

  font {
    capitalization: style === kTitleTertiary ? Font.AllUppercase : Font.MixedCase
    
    letterSpacing: {
      switch (style) {
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
