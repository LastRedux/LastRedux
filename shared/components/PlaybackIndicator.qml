import QtQuick 2.14

Item {
  id: root

  property int bottomPosition: isLarge ? 3 : 2
  property int topPosition: isLarge ? 17 : 10
  property int barOffset: isLarge ? 7 : 4
  
  property bool isLarge: false
  property bool isPaused: false

  width: isLarge ? 31 : 18
  height: isLarge ? 31 : 18

  Image {
    source: `../resources/playbackIndicatorBackground${isLarge ? '-large' : ''}.png`

    anchors {
      fill: parent

      margins: -6
    }
  }

  PlaybackIndicatorBar {
    index: 0

    x: barOffset * 1
  }

  PlaybackIndicatorBar {
    index: 1
    
    x: barOffset * 2
  }

  PlaybackIndicatorBar {
    index: 2
    
    x: barOffset * 3
  }
}