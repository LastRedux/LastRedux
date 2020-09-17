import QtQuick.Controls 2.14
import QtQuick 2.14

import '../../shared/components'

Item { 
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

      Label {
        horizontalAlignment: Qt.AlignHCenter
        text: 'Connecting to Last.fm... 🚀'
        style: kLargeTitle

        width: parent.width
      }

      Label {
        horizontalAlignment: Qt.AlignHCenter
        textFormat: Text.StyledText
        text: 'Authorize LastRedux by clicking <b>Yes, Allow Access</b> on Last.fm. If a webpage didn’t open, click <b>Try Again</b> or copy and paste this link into your browser:'
        lineHeight: 1.25
        wrapMode: Text.Wrap

        width: parent.width
      }

      SelectableText {
        horizontalAlignment: Qt.AlignHCenter
        text: 'https://www.last.fm/api/auth?api_key=XXXXXXXXXXX&token=XXXXXXXXXXX'
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
      }

      LabelButton {
        style: kPrimary
        title: 'Continue'
      }
    }
  }
}