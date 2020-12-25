import QtQuick.Controls 2.14
import QtQuick 2.14

import '../../shared/components'

Item {
  id: root

  property var authUrl
  property bool hasError

  signal back
  signal tryAgain
  signal tryAuthenticating

  Item {
    anchors {
      top: parent.top
      right: parent.right
      bottom: buttonContainer.top
      left: parent.left
    }

    Column {
      width: 512
      spacing: 15

      anchors.centerIn: parent

      Item {
        x: parent.width / 2 - (width / 2)
        width: 313
        height: 85

        Image {
          source: '../../shared/resources/onboarding-connecting.png'

          width: 353
          height: 125

          anchors.centerIn: parent
        }
      }

      Label {
        horizontalAlignment: Qt.AlignHCenter
        text: hasError ? 'Error Connecting ⚠️' : 'Connect to Last.fm 🚀'
        style: kLargeTitle

        width: parent.width
      }

      Label {
        horizontalAlignment: Qt.AlignHCenter
        textFormat: Text.StyledText
        lineHeight: 1.25
        wrapMode: Text.Wrap

        text: {
          if (hasError) {
            return 'LastRedux didn\'t detect that you logged into your Last.fm account. Click <b>Try Again</b>, then click <b>Yes, Allow Access</b> on Last.fm.'
          }
          
          return `Authorize LastRedux by clicking <b>Yes, Allow Access</b> on Last.fm.${authUrl ? ' If a webpage didn’t open, click <b>Try Again</b> or copy and paste this link into your browser:' : ''}`
        }

        width: parent.width
      }

      SelectableText {
        horizontalAlignment: Qt.AlignHCenter
        isContextMenuEnabled: false // Context menus aren't supported in modals as of Qt 5.15
        text: authUrl
        visible: authUrl

        width: parent.width
      }
    }
  }

  Image {
    id: buttonContainer

    fillMode: Image.TileHorizontally
    source: '../../shared/resources/onboardingButtonContainerBackground.png'
    
    height: 58
    
    anchors {
      right: parent.right
      bottom: parent.bottom
      left: parent.left
    }

    LabelButton {
      style: kBack
      title: 'Back'

      onClicked: root.back()

      anchors {
        left: parent.left
        verticalCenter: parent.verticalCenter
        
        leftMargin: 15
      }
    }

    Row {
      spacing: 12
      
      anchors {
        right: parent.right
        verticalCenter: parent.verticalCenter
        
        rightMargin: 15
      }
      
      LabelButton {
        title: 'Try Again'

        onClicked: root.tryAgain()
      }

      LabelButton {
        style: kPrimary
        title: 'I\'ve Logged In'

        onClicked: root.tryAuthenticating()
      }
    }
  }
}