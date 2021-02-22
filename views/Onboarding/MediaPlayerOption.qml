import QtQuick 2.14

Item {
  property string iconName
  property bool isActive: false

  signal activated

  width: 150
  height: width

  Image {
    opacity: mouseArea.containsPress ? 0.625 : 1
    source: '../../shared/resources/onboarding-mediaPlayerSelection.png'
    visible: isActive || mouseArea.containsPress

    anchors.fill: parent
  }

  Image {
    source: `../../shared/resources/onboarding-${iconName}.png`
    anchors.centerIn: parent
  }

  MouseArea {
    id: mouseArea

    onClicked: if (!isActive) { activated() }

    anchors.fill: parent
  }
}