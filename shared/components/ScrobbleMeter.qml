import QtQuick 2.14
import QtQuick.Controls 2.14 as Controls

Row {
  property alias percentage: progressBar.percentage

  spacing: 5

  height: logo.height

  ProgressBar {
    id: progressBar

    isLastFm: true

    width: 43
    height: 5

    y: logo.height / 2 - (height / 2)
  }

  Item {
    id: logo

    width: 17
    height: 9

    Image {
      source: `../resources/scrobbleMeterLogo-${percentage === 1 ? '' : 'de'}activated.png`
      
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