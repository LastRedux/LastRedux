import QtQuick 2.14

Item {
  id: root

  property bool isLastFm
  property real percentage

  width: 43
  height: 5

  // --- Background ---

  BorderImage {
    horizontalTileMode: BorderImage.Repeat
    source: '../resources/progressBar.png'

    border {
      top: 10
      right: 11
      bottom: 10
      left: 11
    }

    anchors {
      fill: parent

      margins: -8
    }
  }

  // --- Fill ---
  
  Item {
    width: percentage * parent.width
    height: parent.height

    BorderImage {
      source: `../resources/progressBarFill${isLastFm ? '-lastfm' : ''}.png`

      border {
        top: 2
        right: 11
        bottom: 2
        left: 3
      }
      
      anchors {
        fill: parent

        rightMargin: -8
      }
    }
  }
}