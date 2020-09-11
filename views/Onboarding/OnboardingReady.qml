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
      spacing: 30

      anchors.centerIn: parent

      Item {
        x: parent.width / 2 - (width / 2) // Center horizontally
        width: 284
        height: 109

        Image {
          source: '../../shared/resources/trayIconPreview-macOSCatalina.png'

          anchors {
            fill: parent

            margins: -45
          }
        }
      }

      Column {
        spacing: 15

        width: parent.width

        Label {
          textFormat: Text.RichText
          horizontalAlignment: Qt.AlignHCenter
          text: 'LastRedux is ready 🔥'
          style: kLargeTitle

          width: parent.width
        }

        Label {
          horizontalAlignment: Qt.AlignHCenter
          textFormat: Text.RichText
          text: 'LastRedux lives in your Mac’s status bar. Reopen the LastRedux window by<br>clicking the icon and selecting <b>Show Window</b>.'
          lineHeight: 1.1
          wrapMode: Text.Wrap

          width: parent.width
        }

        Label {
          horizontalAlignment: Qt.AlignHCenter
          textFormat: Text.RichText
          text: 'If you have questions or bug reports, please share them on <a href="https://github.com/LastRedux/LastRedux">our GitHub</a>.'

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
      text: 'Finish'

      anchors {
        right: parent.right
        verticalCenter: parent.verticalCenter
        
        rightMargin: 20
      }
    }
  }
}