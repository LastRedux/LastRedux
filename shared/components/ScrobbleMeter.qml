import QtQuick 2.15
import QtQuick.Controls 2.15 as Controls

Row {
  property real percentage: 0

  spacing: 5

  height: logo.height

  Item {
    width: 40
    height: 5

    y: logo.height / 2 - (height / 2)
    
    BorderImage {
      horizontalTileMode: BorderImage.Repeat
      source: '../resources/scrobbleMeterBackground.png'

      border {
        top: 4
        right: 5
        bottom: 6
        left: 5
      }

      anchors {
        fill: parent

        topMargin: -2
        rightMargin: -3
        bottomMargin: -4
        leftMargin: -3
      }
    }

    Item {
      width: percentage * parent.width
      height: parent.height

      BorderImage {
        horizontalTileMode: BorderImage.Repeat
        source: '../resources/scrobbleMeterFill.png'

        border {
          top: 2
          right: 10
          bottom: 2
          left: 2
        }

        anchors {
          fill: parent

          rightMargin: -8
        }
      }
    }

    MouseArea {
      id: mouseArea

      hoverEnabled: true

      anchors.fill: parent
    }
  }

  Item {
    id: logo

    width: 17
    height: 9

    Image {
      source: `../resources/scrobbleMeterLogo${percentage === 1 ? 'A' : 'Dea'}ctivated.png`
      anchors {
        fill: parent

        topMargin: -2
        rightMargin: -3
        bottomMargin: -4
        leftMargin: -3
      }
    }
  }
}