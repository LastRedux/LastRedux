import QtQuick 2.14

import '../../shared/components'

Item {
  id: root

  signal nextPage

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
        width: 170
        height: width

        x: (parent.width / 2) - (width / 2)

        Image {
          source: '../../shared/resources/onboarding-logo.png'

          anchors {
            fill: parent

            margins: -100
          }
        }
      }

      Column {
        width: parent.width
        spacing: 15

        Label {
          horizontalAlignment: Qt.AlignHCenter
          text: 'Welcome to LastRedux ✨'
          style: kLargeTitle

          width: parent.width
        }

        Label {
          horizontalAlignment: Qt.AlignHCenter
          lineHeight: 1.25
          textFormat: Text.StyledText
          text: 'Connect to Last.fm to track your listening activity on this Mac.<br>If you don’t have a Last.fm account yet, you can create one <b><a href="https://www.last.fm/join">here</a></b>.'
          style: kBodyPrimarySystem
          
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

    // LabelButton {
    //   title: 'Use Without Account'

    //   anchors {
    //     left: parent.left
    //     verticalCenter: parent.verticalCenter
        
    //     leftMargin: 20
    //   }
    // }

    LabelButton {
      style: kPrimary
      title: 'Connect to Last.fm'

      onClicked: root.nextPage()

      anchors {
        right: parent.right
        verticalCenter: parent.verticalCenter
        
        rightMargin: 20
      }
    }
  }
}