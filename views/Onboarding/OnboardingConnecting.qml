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
        textFormat: Text.RichText
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

  Rectangle {
    id: buttonContainer

    color: '#171717'
    height: 60
    
    anchors {
      right: parent.right
      bottom: parent.bottom
      left: parent.left
    }

    Button {
      text: 'Back'

      anchors {
        left: parent.left
        verticalCenter: parent.verticalCenter
        
        leftMargin: 20
      }
    }

    Row {
      spacing: 12
      
      anchors {
        right: parent.right
        verticalCenter: parent.verticalCenter
        
        rightMargin: 20
      }
      
      Button {
        text: 'Try Again'
      }

      Button {
        text: 'Continue'
      }
    }
  }
}