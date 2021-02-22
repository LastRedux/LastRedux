import QtQuick 2.14

import '../../shared/components'

Item {
  id: root

  property string selectedMediaPlayer

  signal mediaPlayerOptionSelected(string mediaPlayerName)
  signal nextPage

  Item {
    anchors {
      top: parent.top
      right: parent.right
      bottom: buttonContainer.top
      left: parent.left
    }

    Column {
      spacing: 30

      anchors.centerIn: parent

      width: 512

      Column {
        spacing: 10
        
        width: parent.width

        Label {
          horizontalAlignment: Qt.AlignHCenter
          text: 'Choose Your Media Player'
          style: kLargeTitle
          width: parent.width
        }

        Label {
          horizontalAlignment: Qt.AlignHCenter
          style: kBodyPrimarySystem
          text: 'You can change this later in the status bar menu.'

          width: parent.width
        }
      }

      Item {
        width: parent.width
        height: 150
        
        Row {
          id: row

          spacing: 30

          anchors.horizontalCenter: parent.horizontalCenter

          height: parent.height

          MediaPlayerOption {
            iconName: 'macOSMusicLogo'
            isActive: selectedMediaPlayer === 'musicApp'

            onActivated: mediaPlayerOptionSelected('musicApp')
          }

          MediaPlayerOption {
            iconName: 'spotifyLogo'
            isActive: selectedMediaPlayer === 'spotify'

            onActivated: mediaPlayerOptionSelected('spotify')
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
      isEnabled: selectedMediaPlayer
      style: kPrimary
      title: 'Continue'

      onClicked: root.nextPage()

      anchors {
        right: parent.right
        verticalCenter: parent.verticalCenter
        
        rightMargin: 15
      }
    }
  }
}