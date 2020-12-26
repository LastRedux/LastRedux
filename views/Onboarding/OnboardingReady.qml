import QtQuick 2.14

import '../../shared/components'

Item {
  id: root

  signal finish

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
        width: 289
        height: 134

        Image {
          source: '../../shared/resources/onboarding-trayIconPreview.png'

          anchors {
            fill: parent

            margins: -40
          }
        }
      }

      Column {
        spacing: 15

        width: parent.width

        Label {
          horizontalAlignment: Qt.AlignHCenter
          text: 'LastRedux Is Ready! 💎'
          style: kLargeTitle

          width: parent.width
        }

        Label {
          horizontalAlignment: Qt.AlignHCenter
          textFormat: Text.StyledText
          text: 'LastRedux lives in your Mac’s status bar. Reopen the LastRedux window by<br>clicking the icon and selecting <b>Show Window</b>.'
          lineHeight: 1.1
          style: kBodyPrimarySystem
          wrapMode: Text.Wrap

          width: parent.width
        }

        Label {
          horizontalAlignment: Qt.AlignHCenter
          lineHeight: 1.1
          textFormat: Text.StyledText
          text: 'If you encounter any bugs, please share them in the <b>#beta-bugs</b> channel in the LastRedux Beta Discord server.'
          style: kBodyPrimarySystem
          wrapMode: Text.Wrap

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
      style: kPrimary
      title: 'Finish'

      onClicked: root.finish()

      anchors {
        right: parent.right
        verticalCenter: parent.verticalCenter
        
        rightMargin: 15
      }
    }
  }
}