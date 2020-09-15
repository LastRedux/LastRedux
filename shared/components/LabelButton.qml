import QtQuick 2.14

Button {
  id: root

  readonly property int rightEdgeInset: isCompact ? 10 : 14
  readonly property int leftEdgeInset: style === kBack ? rightEdgeInset + 5 : rightEdgeInset

  property alias title: label.text

  property int calculatedWidth: leftEdgeInset + label.width + rightEdgeInset

  width: calculatedWidth
  
  Label {
    id: label

    horizontalAlignment: Qt.AlignHCenter
    verticalAlignment: Qt.AlignVCenter
    isShadowEnabled: root.style !== kPrimary
    style: root.isCompact ? kBodyPrimary : kTitleSecondary

    x: leftEdgeInset

    width: root.width === calculatedWidth ? undefined : parent.width - (leftEdgeInset + rightEdgeInset)

    height: parent.height
  }
}