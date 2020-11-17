import QtQuick 2.15

import '../../shared/components'

Item {
  id: root

  property var address
  property string backgroundImageSource
  property string imageSource
  property string username
  property string fullName

  // Apply opacity to all content
  property real contentOpacity: pointerHandlers.containsPress ? 0.5 : 1

  height: avatar.y + avatar.height + 10

  LinkPointerHandlers {
    id: pointerHandlers

    address: root.address

    text: {
      if (root.fullName) {
        return `${root.username} (${root.fullName})`
      }

      return root.username
    }

    anchors.fill: parent
  }

  PictureBackground {
    isBlurEnabled: false
    source: backgroundImageSource

    anchors.fill: parent
  }

  // --- Avatar ---

  Picture {
    id: avatar

    opacity: contentOpacity
    type: kUser
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

    Placeholder {
      visible: !username

      width: 81
      height: 16
    }

    // --- Username ---

    Label {
      id: usernameLabel

      elide: Text.ElideRight
      style: kTitleSecondary
      text: root.username
      visible: username

      width: parent.width
    }

    // --- Real Name ---

    Label {
      id: realNameLabel

      color: Qt.rgba(1, 1, 1, 0.81)
      elide: Text.ElideRight
      style: kBodyPrimary
      text: root.fullName
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