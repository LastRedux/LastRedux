import QtQuick 2.14

import 'Profile'

Item {
  id: root

  // --- User Link ---
  
  UserLink {
    id: userLink

    // address:
    // fullName:
    // username:

    anchors {
      top: parent.top
      right: parent.right
      left: parent.left

      topMargin: 10
    }
  }

  Column {
    id: profileStatistics
    
    spacing: 8

    anchors {
      top: userLink.bottom
      right: parent.right
      left: parent.left

      topMargin: 10
      rightMargin: 15
      leftMargin: 15
    }

    // --- Scrobbles ---

    ProfileStatistic {
      iconName: 'scrobble'
      text: `x scrobbles`

      width: parent.width
    }

    // --- Plays per day ---

    ProfileStatistic {
      iconName: 'clock'
      text: `x plays per day`

      width: parent.width
    }

    // --- Plays per day ---

    ProfileStatistic {
      iconName: 'artist'
      text: `x artists in library`

      width: parent.width
    }

    // --- Plays per day ---

    ProfileStatistic {
      iconName: 'heart'
      text: `x loved tracks`

      width: parent.width
    }
  }

  // --- Tabs ---

  Row {
    id: tabs

    spacing: 5

    anchors {
      horizontalCenter: parent.horizontalCenter

      top: profileStatistics.bottom

      topMargin: 15
    }

    Tab {
      title: 'Tracks'
    }

    Tab {
      title: 'Artists'
    }

    Tab {
      title: 'Albums'
    }
  }
}