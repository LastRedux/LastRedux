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
        text: 'Welcome to LastRedux ✨'
        style: kLargeTitle

        width: parent.width
      }

      Label {
        horizontalAlignment: Qt.AlignHCenter
        textFormat: Text.RichText
        text: 'Connect to Last.fm to track Apple Music listening activity on this Mac.<br>If you don’t have a Last.fm account yet, you can create one <a href="https://www.last.fm/join">here</a>.'
        lineHeight: 1.25
        
        onLinkActivated: Qt.openUrlExternally(link)
        
        width: parent.width

        MouseArea {
          acceptedButtons: Qt.NoButton
          cursorShape: parent.hoveredLink ? Qt.PointingHandCursor : Qt.ArrowCursor

          anchors.fill: parent
        }
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
      text: 'Use Without Account'

      anchors {
        left: parent.left
        verticalCenter: parent.verticalCenter
        
        leftMargin: 20
      }
    }

    Button {
      text: 'Connect to Last.fm 🚀'

      anchors {
        right: parent.right
        verticalCenter: parent.verticalCenter
        
        rightMargin: 20
      }
    }
  }
}