import QtQuick 2.14

Item {
  property alias name: regular.name

  FontLoader {
    id: regular

    source: '../resources/fonts/Inter-Regular.ttf'
  }

  FontLoader {
    source: '../resources/fonts/Inter-Medium.ttf'
  }

  FontLoader {
    source: '../resources/fonts/Inter-SemiBold.ttf'
  }

  FontLoader {
    source: '../resources/fonts/Inter-Bold.ttf'
  }
}
