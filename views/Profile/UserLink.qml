import QtQuick 2.15

import '../../shared/components'

Item {
  id: root

  property var address
  property string imageSource
  property alias username: usernameLabel.text
  property alias fullName: realNameLabel.text

  // Apply opacity to all content
  property real contentOpacity: hoverHandler.hovered && pointHandler.active ? 0.5 : 1

  height: avatar.y + avatar.height + 10

  HoverHandler {
    id: hoverHandler

    cursorShape: address ? Qt.PointingHandCursor : Qt.ArrowCursor
  }

  // TODO: Add context menu
  PointHandler {
    id: pointHandler

    enabled: !!address
  }
  
  TapHandler {
    acceptedButtons: Qt.LeftButton

    onTapped: {
      if (root.address) {
        Qt.openUrlExternally(root.address)
      }
    }
  }

  PictureBackground {
    isBlurEnabled: false
    source: imageSource

    anchors.fill: parent
  }

  // --- Avatar ---

  Picture {
    id: avatar

    opacity: contentOpacity
    type: kArtist // TODO: Add user type
    source: imageSource

    anchors {
      top: parent.top
      left: parent.left

      topMargin: 10
      leftMargin: 15
    }
  }

  Column {
    opacity: contentOpacity
    spacing: 2

    anchors {
      verticalCenter: avatar.verticalCenter

      right: externalLinkIcon.right
      left: avatar.right

      topMargin: 2
      rightMargin: 10
      leftMargin: 10
    }

    // --- Username Placeholder ---

    Rectangle {
      opacity: 0.2
      radius: 4
      visible: !username

      width: 81
      height: 16
    }

    // --- Username ---

    Label {
      id: usernameLabel

      elide: Text.ElideRight
      style: kTitleSecondary
      visible: username

      width: parent.width
    }

    // --- Real Name ---

    Label {
      id: realNameLabel

      elide: Text.ElideRight
      opacity: 0.81
      style: kBodyPrimary
      visible: fullName

      width: parent.width
    }
  }

  // --- External Link Icon ---

  Image {
    id: externalLinkIcon

    opacity: 0.5
    source: '../../shared/resources/externalLink.png'

    anchors {
      verticalCenter: parent.verticalCenter

      right: parent.right

      rightMargin: 15
    }

    states: State {
      name: 'hasUsername'
      when: username

      PropertyChanges {
        target: externalLinkIcon
        opacity: contentOpacity
      }
    }

    transitions: Transition {
      id: transition
      
      from: ''
      to: 'hasUsername'

      PropertyAnimation {
        target: externalLinkIcon
        property: 'opacity'
        duration: 450
        easing.type: Easing.OutQuint
      }
    }
  }
}